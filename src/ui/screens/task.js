import { h, clear, toast, fmtDuration, dots, WORLD_ICON, modKey, debounce, openDialog } from "../dom.js";
import { renderCardBody } from "./card.js";
import { createEditor } from "../../editor/editor.js";
import { lineDiff } from "../../core/diff.js";
import { renderMismatch } from "../mismatch.js";
import { uuid } from "../../core/store.js";
import { randomFrom } from "../i18n.js";
import { markSessionStep, recordDiagnosticResult, draftKey } from "../../core/state.js";

const DRILL = new Set(["retype", "cloze"]);

export async function renderTask(ctx, root, param, query) {
  const { t, pick, content } = ctx;
  const task = content.tasks[param];
  if (!task) { root.append(h("p", { class: "muted" }, t("task.notFound"))); return; }

  const mode = query.mode || "free";
  const sessionDate = query.date || null;
  const stepIndex = query.step !== undefined && query.step !== "" ? Number(query.step) : null;
  const isDrill = DRILL.has(task.type);
  const isDiagnostic = mode === "diagnostic";
  const pasteAllowed = () => !isDrill && !isDiagnostic && !!ctx.settings.pasteInLesson;
  const module = content.modules.find((m) => m.id === task.module);
  const hints = (ctx.settings.lang === "ru" ? task.hints_ru : task.hints_en) || task.hints_en || [];
  const now = () => new Date().toISOString();

  const attempt = {
    id: uuid(), taskId: task.id, variant: 0, type: task.type, mode,
    startedAt: now(), endedAt: null, activeSec: 0, runs: 0, hiddenRuns: 0,
    result: null, testsPassed: 0, testsTotal: 0, hintsUsed: 0, revealedSolution: false, pasted: false,
    errors: [], firstFail: null, code: "", selfRating: null, note: "", cardPeeks: 0,
  };
  const errorCounts = {};
  let finished = false;
  let hintsShown = 0;

  const draft = await ctx.store.kvGet(draftKey(task.id), null);
  const initialDoc = typeof draft === "string" && draft.trim() ? draft : task.starter;

  // ------------------------------------------------------------------ header
  const timerEl = h("span", { class: "chip timer" }, "0:00");
  root.append(h("div", { class: "task-header" },
    h("div", { class: "task-title" },
      h("span", { class: `badge type-${task.type}` }, t(`task.type.${task.type}`)),
      h("h1", {}, task.title)),
    h("div", { class: "task-meta" },
      h("span", { class: "chip", title: t("task.difficulty", { n: task.difficulty }) }, dots(task.difficulty)),
      h("span", { class: "chip" }, t("task.minutes", { n: task.minutes })),
      h("span", { class: "chip" }, `${WORLD_ICON[task.world] || ""} ${task.world}`),
      module ? h("span", { class: "chip muted" }, pick(module, "title")) : null,
      module && !isDiagnostic ? h("button", { class: "btn btn-ghost small card-btn", type: "button", title: pick(module, "title"), onclick: openCard }, `📖 ${t("task.card")}`) : null,
      timerEl),
  ));

  // ------------------------------------------------------------------ left panel
  const panes = {};
  const tabBar = h("div", { class: "tabs", role: "tablist" });
  function addTab(key, label, pane) {
    panes[key] = pane;
    pane.classList.add("pane");
    pane.hidden = true;
    const btn = h("button", { class: "tab", role: "tab", "data-tab": key, onclick: () => switchTab(key) }, label);
    tabBar.append(btn);
  }
  function switchTab(key) {
    for (const [k, pane] of Object.entries(panes)) pane.hidden = k !== key;
    tabBar.querySelectorAll(".tab").forEach((b) => b.classList.toggle("active", b.dataset.tab === key));
  }

  addTab("statement", t("task.statement"), h("div", {},
    h("p", { class: "help" }, t(`task.help.${task.type}`)),
    task.story_en ? h("p", { class: "story-line" }, task.story_en) : null,
    h("p", { class: "statement" }, task.statement_en),
    task.type === "task" && task.starter ? h("pre", { class: "code small" }, h("code", {}, task.starter.trim())) : null,
  ));

  let modelPane = null;
  if (task.type === "retype") {
    modelPane = h("div", {}, h("pre", { class: "code" }, h("code", {}, task.model.trim())), h("div", { class: "diff" }));
    addTab("model", t("task.model"), modelPane);
  }
  if (task.examples?.length) {
    addTab("examples", t("task.examples"), h("div", {}, h("ul", { class: "examples" }, task.examples.map((ex) =>
      h("li", {}, h("code", {}, ex.call), " → ", h("code", {}, "prints" in ex ? JSON.stringify(ex.prints) : ex.expected))))));
  }

  const hintList = h("ol", { class: "hint-list" });
  const hintBtn = h("button", { class: "btn small" }, "");
  const solutionBox = h("div", { class: "solution-box" });
  const revealBtn = h("button", { class: "btn btn-ghost small", onclick: revealSolution }, t("task.solution.show"));
  revealBtn.hidden = true;
  function updateHintButton() {
    if (hintsShown >= hints.length) { hintBtn.textContent = t("task.hint.none"); hintBtn.disabled = true; revealBtn.hidden = false; }
    else hintBtn.textContent = t("task.hint.show", { n: hintsShown + 1, total: hints.length });
  }
  hintBtn.addEventListener("click", showHint);
  updateHintButton();
  if (!isDiagnostic) addTab("hints", `${t("task.hints")} (${hints.length})`, h("div", {}, hintList, h("div", { class: "row" }, hintBtn, revealBtn), solutionBox));

  if (!isDrill && task.talk_track?.length && !isDiagnostic) {
    addTab("talk", t("task.talk"), h("div", {},
      h("ul", {}, task.talk_track.map((line) => h("li", {}, line))),
      task.complexity ? h("p", { class: "muted" }, `${t("task.complexity")}: ${task.complexity}`) : null));
  }

  // ------------------------------------------------------------------ right panel
  const runBtn = h("button", { class: "btn btn-primary", onclick: () => runCode() }, `${t("task.run")} `, h("kbd", {}, `${modKey()}↵`));
  const testBtn = h("button", { class: "btn", onclick: () => runTests() }, `${t("task.tests")} `, h("kbd", {}, `⇧${modKey()}↵`));
  const resetBtn = h("button", { class: "btn btn-ghost", onclick: resetCode }, t("task.reset"));
  const giveUpBtn = h("button", { class: "btn btn-ghost danger", onclick: giveUp }, isDiagnostic ? t("task.skip") : t("task.giveup"));
  const editorHost = h("div", { class: "editor-host" });
  const results = h("div", { class: "results" }, h("p", { class: "muted small" }, t(`task.help.${task.type}`)));
  const actions = h("div", { class: "task-actions" });

  root.append(h("div", { class: "task-grid" },
    h("section", { class: "panel left" }, tabBar, ...Object.values(panes)),
    h("section", { class: "panel right" }, h("div", { class: "toolbar" }, runBtn, testBtn, resetBtn, giveUpBtn), editorHost, results, actions),
  ));
  switchTab("statement");

  const editor = createEditor({
    parent: editorHost, doc: initialDoc, dark: ctx.isDark(), coderpad: ctx.settings.coderpad,
    closeBrackets: ctx.settings.closeBrackets,
    onRun: () => runCode(), onTests: () => runTests(),
    onChange: debounce((code) => { if (!finished) ctx.store.kvSet(draftKey(task.id), code); }, 1500),
    pasteAllowed,
    onPaste: () => { attempt.pasted = true; ctx.logEvent("paste", task.id); toast(t("task.pasteLogged"), "warn"); },
    onPasteBlocked: () => { ctx.logEvent("paste-blocked", task.id); toast(t("task.pasteBlocked"), "warn"); },
  });
  editor.focus();
  const offTheme = ctx.on("theme", () => editor.setDark(ctx.isDark()));
  const offSettings = ctx.on("settings", (s) => { editor.setDark(ctx.isDark()); editor.setCoderpad(s.coderpad); editor.setCloseBrackets(s.closeBrackets); });

  const timer = setInterval(() => {
    if (!finished && document.visibilityState === "visible") { attempt.activeSec += 1; timerEl.textContent = fmtDuration(attempt.activeSec); }
  }, 1000);

  // ------------------------------------------------------------------ helpers
  function noteError(err) { if (err && err.type) errorCounts[err.type] = (errorCounts[err.type] || 0) + 1; }
  function errorsArray() { return Object.entries(errorCounts).map(([type, count]) => ({ type, count })); }
  function describeError(err) {
    return err.line != null ? t("task.errorAt", { type: err.type, line: err.line, message: err.message }) : t("task.errorNoLine", { type: err.type, message: err.message });
  }
  function runtimeReady() {
    if (ctx.runtime.status === "ready" || ctx.runtime.status === "busy") return true;
    toast(t("task.runtimeNotReady"));
    return false;
  }
  function setBusy(flag) { runBtn.disabled = testBtn.disabled = flag; root.classList.toggle("busy", flag); }
  function openCard() {
    attempt.cardPeeks += 1;
    ctx.logEvent("cardPeek", task.id, { module: module.id, n: attempt.cardPeeks });
    openDialog({ title: `${t("card.title")} · L${module.level}`, body: renderCardBody(ctx, module), closeLabel: t("card.close") });
  }

  function outputBlock(res) {
    const box = h("div", { class: "output" }, h("h4", {}, t("task.output")));
    if (res.stdout) box.append(h("pre", { class: "stdout" }, res.stdout), res.truncated ? h("p", { class: "muted small" }, t("task.outputTruncated")) : null);
    else box.append(h("p", { class: "muted small" }, t("task.noOutput")));
    if (res.error) box.append(h("div", { class: "error-block" }, describeError(res.error)));
    return box;
  }
  function examplesBlock(examples) {
    if (!examples?.length) return null;
    return h("div", { class: "examples-result" }, h("h4", {}, t("task.examplesResult")),
      h("table", { class: "table" }, h("tbody", {}, examples.map((ex) => h("tr", { class: ex.status },
        h("td", { class: "icon" }, ex.status === "pass" ? "✓" : ex.status === "fail" ? "✗" : "!"),
        h("td", {}, h("code", {}, ex.call)),
        h("td", {}, ex.error ? h("span", { class: "error-text" }, describeError(ex.error))
          : ex.status === "fail" ? renderMismatch(t, ex.expected, ex.actual, ex.mismatch)
          : h("span", {}, `${t("task.wasExpected")} `, h("code", {}, String(ex.expected)))),
      )))));
  }
  function testsList(tests) {
    return h("ul", { class: "tests" }, (tests || []).map((tr) => h("li", { class: `test ${tr.status}` },
      h("span", { class: "icon" }, tr.status === "pass" ? "✓" : tr.status === "fail" ? "✗" : "!"),
      h("span", { class: "label" }, tr.label || tr.name),
      !isDiagnostic && tr.status === "fail" && tr.expected !== undefined
        ? h("div", { class: "detail" }, renderMismatch(t, tr.expected, tr.actual, tr.mismatch))
        : null,
      !isDiagnostic && tr.status === "error" && tr.error ? h("div", { class: "detail error-text" }, describeError(tr.error)) : null,
    )));
  }

  async function runCode() {
    if (finished || !runtimeReady()) return;
    const code = editor.getDoc();
    attempt.runs += 1;
    setBusy(true);
    const res = await ctx.runner.run(code, task.examples || [], { timeoutMs: task.timeout_ms || undefined });
    setBusy(false);
    noteError(res.error);
    for (const ex of res.examples || []) if (ex.error) noteError(ex.error);
    ctx.logEvent("run", task.id, { ok: res.ok, error: res.error?.type || null, ms: res.ms });
    clear(results);
    results.append(h("div", {}, h("div", { class: `result-head ${res.ok ? "pass" : "fail"}` }, `${t("task.runs")}: ${attempt.runs}`), outputBlock(res), examplesBlock(res.examples)));
    if (res.timeout) toast(t("task.timeout", { ms: task.timeout_ms || 5000 }), "warn", 5000);
  }

  async function runTests() {
    if (finished || !runtimeReady()) return;
    const code = editor.getDoc();
    attempt.runs += 1;
    attempt.hiddenRuns += 1;
    setBusy(true);
    const res = await ctx.runner.tests(code, task.tests, { timeoutMs: task.timeout_ms || undefined });
    setBusy(false);
    noteError(res.error);
    for (const tr of res.tests || []) if (tr.error) noteError(tr.error);
    const passed = (res.tests || []).filter((x) => x.status === "pass").length;
    const total = (res.tests || []).length;
    attempt.testsPassed = passed;
    attempt.testsTotal = total;
    const firstFail = (res.tests || []).find((x) => x.status !== "pass");
    if (firstFail && !attempt.firstFail) attempt.firstFail = firstFail.name;
    ctx.logEvent("hiddenRun", task.id, { ok: res.ok, passed, total, error: res.error?.type || null });
    clear(results);
    results.append(
      h("div", { class: `result-head ${res.ok ? "pass" : "fail"}` }, t("task.testsResult", { passed, total }),
        isDiagnostic ? null : h("span", { class: "fun" }, randomFrom(t(res.ok ? "fun.pass" : "fun.fail")))),
      outputBlock(res), testsList(res.tests));
    if (res.timeout) toast(t("task.timeout", { ms: task.timeout_ms || 5000 }), "warn", 5000);
    if (res.ok) await finish("passed", code);
    else if (task.type === "retype" && !isDiagnostic) showDiff();
    else if (isDrill && !isDiagnostic) revealBtn.hidden = false;
  }

  function showDiff() {
    const diff = lineDiff(task.model, editor.getDoc());
    const box = modelPane.querySelector(".diff");
    clear(box);
    if (diff.every((d) => d.type === "same")) return;
    box.append(h("h4", {}, t("task.diff")), h("pre", { class: "diff-pre" }, diff.map((d) =>
      h("div", { class: `diff-line ${d.type}` }, (d.type === "del" ? "− " : d.type === "add" ? "+ " : "  ") + d.text))));
    switchTab("model");
  }

  function showHint() {
    if (hintsShown >= hints.length) return;
    hintList.append(h("li", {}, hints[hintsShown]));
    hintsShown += 1;
    attempt.hintsUsed = hintsShown;
    ctx.logEvent("hint", task.id, { n: hintsShown });
    updateHintButton();
  }

  function solutionBlock() {
    return h("div", {},
      h("h4", {}, t("task.solution")), h("pre", { class: "code" }, h("code", {}, task.solution.trim())),
      task.solution_alt ? [h("h4", {}, t("task.solutionAlt")), h("pre", { class: "code" }, h("code", {}, task.solution_alt.trim()))] : null);
  }
  function levelsBlock(lv) {
    const column = (key) => h("section", { class: `level ${key}` },
      h("h5", {}, t(`task.level.${key}`)),
      h("pre", { class: "code" }, h("code", {}, lv[key].code.trim())),
      h("p", { class: "note" }, pick(lv[key], "note")));
    return h("div", {}, h("h4", {}, t("task.levels")), h("div", { class: "levels" }, column("middle"), column("senior")));
  }
  function revealSolution() {
    if (attempt.revealedSolution) return;
    attempt.revealedSolution = true;
    ctx.logEvent("reveal", task.id);
    clear(solutionBox);
    solutionBox.append(solutionBlock());
    revealBtn.hidden = true;
    switchTab("hints");
  }

  async function finish(result, code) {
    if (finished) return;
    finished = true;
    clearInterval(timer);
    attempt.result = result;
    attempt.endedAt = now();
    attempt.code = code ?? editor.getDoc();
    attempt.errors = errorsArray();
    await ctx.store.putAttempt(attempt);
    await ctx.store.kvDelete(draftKey(task.id));
    ctx.logEvent("finish", task.id, { result, activeSec: attempt.activeSec, hints: attempt.hintsUsed, runs: attempt.runs });
    if (sessionDate && stepIndex !== null) await markSessionStep(ctx.store, sessionDate, stepIndex, { status: "done", attemptId: attempt.id, result });
    if (isDiagnostic) await recordDiagnosticResult(ctx.store, { taskId: task.id, passed: result === "passed", activeSec: attempt.activeSec, runs: attempt.runs, hintsUsed: attempt.hintsUsed });
    editor.setReadOnly(true);
    runBtn.disabled = testBtn.disabled = resetBtn.disabled = giveUpBtn.disabled = true;
    renderOutcome(result);
  }

  function renderOutcome(result) {
    const label = result === "passed" ? t("task.passed") : result === "gaveUp" ? t("task.gaveUp") : t("task.failed");
    const box = h("section", { class: `outcome ${result}` },
      h("h3", {}, `${result === "passed" ? "✓" : "•"} ${label} · ${fmtDuration(attempt.activeSec)}`),
      isDiagnostic ? null : h("p", { class: "fun" }, randomFrom(t(result === "passed" ? "fun.pass" : "fun.gaveUp"))));
    if (!isDiagnostic) {
      box.append(h("h4", {}, t("task.explanation")), h("p", {}, pick(task, "explanation")));
      const lv = task.levels;
      const solutionShownAsLevel = lv && [lv.middle.code, lv.senior.code].some((c) => c.trim() === task.solution.trim());
      if (!solutionShownAsLevel) box.append(solutionBlock());
      if (lv) box.append(levelsBlock(lv));
      if (task.talk_track?.length) box.append(h("h4", {}, t("task.talk")), h("ul", {}, task.talk_track.map((l) => h("li", {}, l))));
      if (task.followups?.length) box.append(h("h4", {}, t("task.followups")), h("ul", {}, task.followups.map((l) => h("li", {}, l))));
    }
    const nextHash = isDiagnostic ? "#/diagnostic" : sessionDate ? "#/session" : "#/map";
    const nextLabel = isDiagnostic ? t("task.toDiagnostic") : sessionDate ? t("task.toSession") : t("task.toMap");
    actions.append(h("a", { class: "btn btn-primary big", href: nextHash }, nextLabel));
    results.append(box);
    box.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  async function giveUp() {
    if (finished) return;
    if (!isDiagnostic && !window.confirm(t("task.giveupConfirm"))) return;
    ctx.logEvent(isDiagnostic ? "skip" : "giveUp", task.id);
    await finish(isDiagnostic ? "failed" : "gaveUp");
  }
  function resetCode() {
    if (finished) return;
    if (!window.confirm(t("task.resetConfirm"))) return;
    editor.setDoc(task.starter);
    ctx.store.kvDelete(draftKey(task.id));
    editor.focus();
  }

  return () => {
    clearInterval(timer);
    offTheme();
    offSettings();
    if (!finished && attempt.runs > 0) {
      attempt.result = "left";
      attempt.endedAt = now();
      attempt.code = editor.getDoc();
      attempt.errors = errorsArray();
      ctx.store.putAttempt(attempt);
    }
    editor.destroy();
  };
}
