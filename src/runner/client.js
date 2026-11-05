/**
 * Runner: the main-thread side of the Pyodide worker.
 *  - serializes requests (one Python run at a time),
 *  - enforces a wall-clock timeout by terminating the worker,
 *  - keeps a pre-warmed spare worker so a killed run recovers in about a second.
 *
 * `createWorker` is injectable so node tests can drive it with a fake worker.
 */

export const DEFAULT_TIMEOUT_MS = 5000;

function defaultCreateWorker() {
  return new Worker(new URL("./worker.js", import.meta.url), { type: "module" });
}

function emptyResult(error, flags = {}) {
  return { ok: false, error, tests: [], examples: [], stdout: "", ...flags };
}

export class Runner {
  constructor({ createWorker = defaultCreateWorker, timeoutMs = DEFAULT_TIMEOUT_MS, onStatus = () => {}, spare = true } = {}) {
    this.createWorker = createWorker;
    this.timeoutMs = timeoutMs;
    this.onStatus = onStatus;
    this.useSpare = spare;
    this.primary = null;        // { worker, python }
    this.sparePromise = null;   // Promise<{worker, python} | null>
    this.startPromise = null;
    this.queue = Promise.resolve();
    this.nextId = 1;
    this.status = "idle";
    this.python = null;
  }

  setStatus(status, extra = {}) {
    this.status = status;
    this.onStatus(status, { python: this.python, ...extra });
  }

  /** Boot the primary worker (and a spare in the background). Safe to call repeatedly. */
  start() {
    if (!this.startPromise) {
      this.startPromise = (async () => {
        this.setStatus("booting");
        try {
          this.primary = await this.spawn();
          this.python = this.primary.python;
          if (this.useSpare) this.sparePromise = this.spawn().catch(() => null);
          this.setStatus("ready");
        } catch (err) {
          this.startPromise = null;
          this.setStatus("error", { message: err.message });
          throw err;
        }
      })();
    }
    return this.startPromise;
  }

  spawn() {
    return new Promise((resolve, reject) => {
      const worker = this.createWorker();
      const cleanup = () => {
        worker.removeEventListener("message", onMessage);
        worker.removeEventListener("error", onError);
      };
      const onMessage = (event) => {
        const msg = event.data || {};
        if (msg.type === "ready") { cleanup(); resolve({ worker, python: msg.python }); }
        else if (msg.type === "boot-error") { cleanup(); worker.terminate(); reject(new Error(msg.message || "worker failed to boot")); }
      };
      const onError = (event) => { cleanup(); worker.terminate(); reject(new Error((event && event.message) || "worker error")); };
      worker.addEventListener("message", onMessage);
      worker.addEventListener("error", onError);
    });
  }

  /** Queue a request; resolves with the harness result (never rejects for Python errors). */
  request(payload, { timeoutMs } = {}) {
    const limit = timeoutMs ?? payload.timeoutMs ?? this.timeoutMs;
    const run = () => this.send(payload, limit);
    const promise = this.queue.then(run, run);
    this.queue = promise.catch(() => {});
    return promise;
  }

  async send(payload, timeoutMs) {
    await this.start();
    const { worker } = this.primary;
    const id = this.nextId++;
    this.setStatus("busy");
    const result = await new Promise((resolve) => {
      let timer = null;
      const finish = (res) => {
        clearTimeout(timer);
        worker.removeEventListener("message", onMessage);
        worker.removeEventListener("error", onError);
        resolve(res);
      };
      const onMessage = (event) => {
        const msg = event.data || {};
        if (msg.type === "response" && msg.id === id) finish({ timeout: false, crashed: false, ...msg.result });
      };
      const onError = (event) => finish(emptyResult(
        { type: "WorkerCrash", message: (event && event.message) || "the Python worker crashed", line: null },
        { crashed: true, timeout: false },
      ));
      worker.addEventListener("message", onMessage);
      worker.addEventListener("error", onError);
      timer = setTimeout(() => finish(emptyResult(
        { type: "Timeout", message: `no result within ${timeoutMs} ms – an infinite loop?`, line: null },
        { timeout: true, crashed: false },
      )), timeoutMs);
      worker.postMessage({ type: "request", id, payload });
    });
    if (result.timeout || result.crashed) await this.replacePrimary();
    else this.setStatus("ready");
    return result;
  }

  async replacePrimary() {
    this.setStatus("restarting");
    try { this.primary.worker.terminate(); } catch { /* already gone */ }
    this.primary = null;
    let next = this.sparePromise ? await this.sparePromise : null;
    this.sparePromise = null;
    if (!next) next = await this.spawn();
    this.primary = next;
    this.python = next.python;
    if (this.useSpare) this.sparePromise = this.spawn().catch(() => null);
    this.setStatus("ready");
  }

  run(code, examples = [], opts) { return this.request({ kind: "run", code, examples }, opts); }
  tests(code, tests, opts) { return this.request({ kind: "tests", code, tests }, opts); }
  scratch(code, reset = false, opts) { return this.request({ kind: "scratch", code, reset }, opts); }
  ping(opts) { return this.request({ kind: "ping" }, opts); }
}
