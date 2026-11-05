import { test } from "node:test";
import assert from "node:assert/strict";
import { Runner } from "../src/runner/client.js";

/** Fake worker: becomes ready on the next tick; a payload whose code contains "hang" never answers. */
class FakeWorker extends EventTarget {
  static created = 0;
  constructor() {
    super();
    FakeWorker.created += 1;
    this.terminated = false;
    setTimeout(() => this.emit({ type: "ready", python: "3.14.2" }), 0);
  }
  emit(data) { const ev = new Event("message"); ev.data = data; this.dispatchEvent(ev); }
  postMessage(msg) {
    if (this.terminated || msg.type !== "request") return;
    if (msg.payload.code && msg.payload.code.includes("hang")) return; // infinite loop: never answers
    setTimeout(() => this.emit({ type: "response", id: msg.id, result: { ok: true, stdout: msg.payload.code, tests: [], examples: [] } }), 5);
  }
  terminate() { this.terminated = true; }
}

test("requests are answered in order and the status settles on ready", async () => {
  FakeWorker.created = 0;
  const statuses = [];
  const runner = new Runner({ createWorker: () => new FakeWorker(), timeoutMs: 200, onStatus: (s) => statuses.push(s) });
  await runner.start();
  const [a, b] = await Promise.all([runner.run("print(1)"), runner.tests("print(2)", "def test_x(ns): pass")]);
  assert.equal(a.stdout, "print(1)");
  assert.equal(b.stdout, "print(2)");
  assert.equal(runner.status, "ready");
  assert.equal(runner.python, "3.14.2");
  assert.equal(FakeWorker.created, 2, "primary plus one spare");
  assert.deepEqual(statuses.slice(0, 2), ["booting", "ready"]);
});

test("a hung run times out, the spare takes over and the next run works", async () => {
  FakeWorker.created = 0;
  const statuses = [];
  const runner = new Runner({ createWorker: () => new FakeWorker(), timeoutMs: 100, onStatus: (s) => statuses.push(s) });
  await runner.start();
  const first = runner.primary.worker;
  const hung = await runner.run("while True: hang");
  assert.equal(hung.ok, false);
  assert.equal(hung.timeout, true);
  assert.equal(hung.error.type, "Timeout");
  assert.equal(first.terminated, true, "the hung worker was killed");
  assert.notEqual(runner.primary.worker, first, "the spare was promoted");
  assert.ok(statuses.includes("restarting"));
  const next = await runner.run("print('ok')");
  assert.equal(next.ok, true);
  assert.equal(FakeWorker.created, 3, "primary, spare, and a fresh spare after the swap");
  assert.equal(runner.status, "ready");
});

test("a request made before start boots the runner first", async () => {
  const runner = new Runner({ createWorker: () => new FakeWorker(), spare: false });
  const res = await runner.run("x = 1");
  assert.equal(res.ok, true);
});
