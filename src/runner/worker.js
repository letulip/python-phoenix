/* Python Phoenix runner worker (ES module worker).
 * Boots Pyodide once from the ESM build via dynamic import(), installs runner.py, then answers
 * {type: "request", id, payload} messages with {type: "response", id, result}.
 * The main thread owns timeouts: it simply terminates this worker and promotes a spare. */

const PYODIDE_VERSION = "314.0.7";
const CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

let runRequest = null;

function notReady(id) {
  postMessage({
    type: "response", id,
    result: { ok: false, error: { type: "NotReady", message: "Python runtime is still loading", line: null }, tests: [], examples: [], stdout: "" },
  });
}

async function boot() {
  try {
    const { loadPyodide } = await import(CDN + "pyodide.mjs");
    const pyodide = await loadPyodide({ indexURL: CDN });
    const response = await fetch(new URL("./runner.py", import.meta.url));
    if (!response.ok) throw new Error(`runner.py: HTTP ${response.status}`);
    pyodide.runPython(await response.text());
    runRequest = pyodide.globals.get("run_request");
    const python = pyodide.runPython("import sys; sys.version.split()[0]");
    postMessage({ type: "ready", python, pyodide: PYODIDE_VERSION });
  } catch (err) {
    postMessage({ type: "boot-error", message: String((err && err.message) || err) });
  }
}

self.onmessage = (event) => {
  const msg = event.data || {};
  if (msg.type !== "request") return;
  if (!runRequest) { notReady(msg.id); return; }
  let result;
  try {
    result = JSON.parse(runRequest(JSON.stringify(msg.payload)));
  } catch (err) {
    result = { ok: false, error: { type: "HarnessError", message: String((err && err.message) || err), line: null }, tests: [], examples: [], stdout: "" };
  }
  postMessage({ type: "response", id: msg.id, result });
};

boot();
