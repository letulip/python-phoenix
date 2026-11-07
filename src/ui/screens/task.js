import { h, clear, toast, fmtDuration, dots, WORLD_ICON, modKey, debounce, openDialog } from "../dom.js";
import { renderCardBody } from "./card.js";
import { gymStepHash, familyOf } from "./gym.js";
import { createEditor } from "../../editor/editor.js";
import { lineDiff } from "../../core/diff.js";
import { renderMismatch } from "../mismatch.js";
import { uuid } from "../../core/store.js";
import { randomFrom } from "../i18n.js";
import { todayKey } from "../../core/progress.js";
import { markSessionStep, recordDiagnosticResult, draftKey, markRoundStep, loadRound, recordGymResult } from "../../core/state.js";

const DRILL = new Set(["retype", "cloze", "rewrite", "predict"]);

/** Predict drills compare printed output: trailing spaces, blank edges and the quote style do not matter. */
export function normalizeAnswer(text) {
  return String(text ?? "").replace(/\r/g, "").split("\n").map((line) => line.trimEnd()).join("\n").trim().replace(/"/g, "'");
}

export async function renderTask(ctx, root, param, query) {
  const { t, pick, content } = ctx;
  const task = content.tasks[param];
  if (!task) { root.append(h("p", { class: "muted" }, t("task.notFound"))); return; }

  const mode = query.mode || "free";
  const isGym = mode === "gym";
  const sessionDate = query.date || null;
  const stepIndex = query.step !== undefined && query.step !== "" ? Number(query.step) : null;
  const variantIndex = Math.max(0, Number(query.variant) || 0);
  const v = task.variants?.[variantIndex] || task; // starter, solution, tests, model, examples, snippet, expected_output
  const isDrill = DRILL.has(task.type);
  const isPredict = task.type === "predict";
  const isDiagnostic = mode === "diagnostic";
  const pasteAllowed = () => !isDrill && !isDiagnostic && !!ctx.settings.pasteInLesson;
  const module = content.modules.find((m) => m.id === task.module);
  const family = task.idiom ? familyOf(content, task.idiom) : null;
  const hints = (ctx.settings.lang === "ru" ? task.hints_ru : task.hints_en) || task.hints_en || [];
  const now = () => new Date().toISOString();

  const attempt = {
    id: uuid(), taskId: task.id, variant: variantIndex, type: task.type, mode,
    startedAt: now(), endedAt: null, activeSec: 0, runs: 0, hiddenRuns: 0,
    result: null, testsPassed: 0, testsTotal: 0, hintsUsed: 0, revealedSolution: false, pasted: false,
    errors: [], firstFail: null, code: "", selfRating: null, note: "", cardPeeks: 0,
  };
  const errorCounts = {};
  let finished = false;
  let hintsShown = 0;

  const draftId = variantIndex ? `${task.id}#${variantIndex}` : task.id;
  const draft = isPredict ? null : await ctx.store.kvGet(draftKey(draftId), null);
  const initialDoc = typeof draft === "string" && draft.trim() ? draft : v.starter;

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
      family ? h("span", { class: "chip muted" }, pick(family, "title")) : null,
      task.variants?.length > 1 ? h("span", { class: "chip muted" }, t("gym.step.variant", { n: variantIndex + 1 })) : null,
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
    isPredict && v.snippet ? h("pre", { class: "code" }, h("code", {}, v.snippet.trim())) : null,
    task.type === "task" && v.starter ? h("pre", { class: "code small" }, h("code", {}, v.starter.trim())) : null,
  ));

  let modelPane = null;
  if (task.type === "retype") {
    modelPane = h("div", {}, h("pre", { class: "code" }, h("code", {}, v.model.trim())), h("div", { class: "diff" }));
    addTab("model", t("task.model"), modelPane);
  }
  if (v.examples?.length) {
    addTab("examples", t("task.examples"), h("div", {}, h("ul", { class: "examples" }, v.examples.map((ex) =>
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
  const giveUpBtn = h("button", { class: "btn btn-ghost danger", onclick: giveUp }, isDiagnostic ? t("task.skip") : t("task.giveup"));
  const results = h("div", { class: "results" }, h("p", { class: "muted small" }, t(`task.help.${task.type}`)));
  const actions = h("div", { class: "task-actions" });
  let runBtn = null, testBtn = null, resetBtn = null, checkBtn = null, editorHost = null, answerEl = null, editor = null;

  if (isPredict) {
    checkBtn = h("button", { class: "btn btn-primary", onclick: () => checkAnswer() }, `${t("task.check")} `, h("kbd", {}, `${modKey()}↵`));
    answerEl = h("textarea", { class: "answer", rows: 4, spellcheck: "false", autocomplete: "off", placeholder: t("task.predict.placeholder") });
    answerEl.addEventListener("keydown", (e) => { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") { e.preventDefault(); checkAnswer(); } });
    answerEl.addEventListener("paste", (e) => { if (!pasteAllowed()) { e.preventDefault(); ctx.logEvent("paste-blocked", task.id); toast(t("task.pasteBlocked"), "warn"); } });
    root.append(h("div", { class: "task-grid" },
      h("section", { class: "panel left" }, tabBar, ...Object.values(panes)),
      h("section", { class: "panel right" }, h("div", { class: "toolbar" }, checkBtn, giveUpBtn), answerEl, results, actions),
    ));
    switchTab("statement");
    answerEl.focus();
  } else {
    runBtn = h("button", { class: "btn btn-primary", onclick: () => runCode() }, `${t("task.run")} `, h("kbd", {}, `${modKey()}↵`));
    testBtn = h("button", { class: "btn", onclick: () => runTests() }, `${t("task.tests")} `, h("kbd", {}, `⇧${modKey()}↵`));
    resetBtn = h("button", { class: "btn btn-ghost", onclick: resetCode }, t("task.reset"));
    editorHost = h("div", { class: "editor-host" });
    root.append(h("div", { class: "task-grid" },
      h("section", { class: "panel left" }, tabBar, ...Object.values(panes)),
      h("section", { class: "panel right" }, h("div", { class: "toolbar" }, runBtn, testBtn, resetBtn, giveUpBtn), editorHost, results, actions),
    ));
    switchTab("statement");
    editor = createEditor({
      parent: editorHost, doc: initialDoc, dark: ctx.isDark(), coderpad: ctx.settings.coderpad,
      closeBrackets: ctx.settings.closeBrackets,
      onRun: () => runCode(), onTests: () => runTests(),
      onChange: debounce((code) => { if (!finished) ctx.store.kvSet(draftKey(draftId), code); }, 1500),
      pasteAllowed,
      onPaste: () => { attempt.pasted = true; ctx.logEvent("paste", task.id); toast(t("task.pasteLogged"), "warn"); },
      onPasteBlocked: () => { ctx.logEvent("paste-blocked", task.id); toast(t("task.pasteBlocked"), "warn"); },
    });
    editor.focus();
  }
  const offTheme = ctx.on("theme", () => editor?.setDark(ctx.isDark()));
  const offSettings = ctx.on("settings", (s) => { if (!editor) return; editor.setDark(ctx.isDark()); editor.setCoderpad(s.coderpad); editor.setCloseBrackets(s.closeBrackets); });

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
  function setBusy(flag) { if (runBtn) runBtn.disabled = testBtn.disabled = flag; root.classList.toggle("busy", flag); }
  function currentCode() { return editor ? editor.getDoc() : (answerEl ? answerEl.value : ""); }
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
    if (finished || isPredict || !runtimeReady()) return;
    const code = editor.getDoc();
    attempt.runs += 1;
    setBusy(true);
    const res = await ctx.runner.run(code, v.examples || [], { timeoutMs: task.timeout_ms || undefined });
    setBusy(false);
    noteError(res.error);
    for (const ex of res.examples || []) if (ex.error) noteError(ex.error);
    ctx.logEvent("run", task.id, { ok: res.ok, error: res.error?.type || null, ms: res.ms });
    clear(results);
    results.append(h("div", {}, h("div", { class: `result-head ${res.ok ? "pass" : "fail"}` }, `${t("task.runs")}: ${attempt.runs}`), outputBlock(res), examplesBlock(res.examples)));
    if (res.timeout) toast(t("task.timeout", { ms: task.timeout_ms || 5000 }), "warn", 5000);
  }

  async function runTests() {
    if (finished || isPredict || !runtimeReady()) return;
    const code = editor.getDoc();
    attempt.runs += 1;
    attempt.hiddenRuns += 1;
    setBusy(true);
    const res = await ctx.runner.tests(code, v.tests, { timeoutMs: task.timeout_ms || undefined });
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

  /** Predict drills: the answer is the printed output, compared after normalisation. */
  async function checkAnswer() {
    if (finished || !isPredict) return;
    const answer = answerEl.value;
    if (!answer.trim()) { answerEl.focus(); return; }
    attempt.runs += 1;
    attempt.hiddenRuns += 1;
    const expected = v.expected_output || "";
    const ok = normalizeAnswer(answer) === normalizeAnswer(expected);
    attempt.testsPassed = ok ? 1 : 0;
    attempt.testsTotal = 1;
    if (!ok && !attempt.firstFail) attempt.firstFail = "output";
    ctx.logEvent("hiddenRun", task.id, { ok, passed: ok ? 1 : 0, total: 1, error: null, variant: variantIndex });
    clear(results);
    results.append(h("div", { class: `result-head ${ok ? "pass" : "fail"}` }, t("task.testsResult", { passed: ok ? 1 : 0, total: 1 }),
      isDiagnostic ? null : h("span", { class: "fun" }, randomFrom(t(ok ? "fun.pass" : "fun.fail")))));
    if (ok) { await finish("passed", answer); return; }
    results.append(h("div", { class: "detail" }, renderMismatch(t, expected.trimEnd(), answer.replace(/\r/g, "").trimEnd(), { kind: "str" })));
    if (attempt.runs >= 2 && !isDiagnostic) revealBtn.hidden = false;
    answerEl.focus();
  }

  function showDiff() {
    const diff = lineDiff(v.model, editor.getDoc());
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
    if (isPredict) return h("div", {}, h("h4", {}, t("task.predict.expected")), h("pre", { class: "code" }, h("code", {}, (v.expected_output || "").trim())));
    return h("div", {},
      h("h4", {}, t("task.solution")), h("pre", { class: "code" }, h("code", {}, (v.solution || "").trim())),
      variantIndex === 0 && task.solution_alt ? [h("h4", {}, t("task.solutionAlt")), h("pre", { class: "code" }, h("code", {}, task.solution_alt.trim()))] : null);
  }
  function levelsBlock(lv) {
    const column = (key) => h("section", { class: `level ${key}` },
      h("h5", {}, t(`task.level.${key}`)),
      h("pre", { class: "code" }, h("code", {}, lv[key].code.trim())),
      h("p", { class: "note" }, pick(lv[key], "note")));
    return h("div", {}, h("h4", {}, t("task.levels")), h("div", { class: "levels" }, column("middle"), column("senior")));
  }
  function ruleBox() {
    if (!family) return null;
    return h("section", { class: "rule-box" },
      h("h4", {}, t("gym.rule")),
      h("p", { class: "rule-title" }, pick(family, "title")),
      h("p", {}, pick(family, "rule")),
      family.phrase_en ? h("p", { class: "quote" }, `“${family.phrase_en}”`) : null);
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

  async function nextNavigation() {
    if (isDiagnostic) return { hash: "#/diagnostic", label: t("task.toDiagnostic") };
    if (isGym) {
      const round = await loadRound(ctx.store);
      const next = round ? round.steps.findIndex((s) => s.status === "pending") : -1;
      return next >= 0 ? { hash: gymStepHash(round.steps[next], next), label: t("gym.next") } : { hash: "#/gym/round", label: t("gym.finish") };
    }
    if (sessionDate) return { hash: "#/session", label: t("task.toSession") };
    return { hash: "#/map", label: t("task.toMap") };
  }

  async function finish(result, code) {
    if (finished) return;
    finished = true;
    clearInterval(timer);
    attempt.result = result;
    attempt.endedAt = now();
    attempt.code = code ?? currentCode();
    attempt.errors = errorsArray();
    await ctx.store.putAttempt(attempt);
    if (!isPredict) await ctx.store.kvDelete(draftKey(draftId));
    ctx.logEvent("finish", task.id, { result, activeSec: attempt.activeSec, hints: attempt.hintsUsed, runs: attempt.runs, variant: variantIndex });
    if (sessionDate && stepIndex !== null) await markSessionStep(ctx.store, sessionDate, stepIndex, { status: "done", attemptId: attempt.id, result });
    if (isGym && stepIndex !== null) await markRoundStep(ctx.store, stepIndex, { status: "done", attemptId: attempt.id, result });
    if (task.idiom && !isDiagnostic) await recordGymResult(ctx.store, task.id, result === "passed", todayKey(), attempt.endedAt);
    if (isDiagnostic) await recordDiagnosticResult(ctx.store, { taskId: task.id, passed: result === "passed", activeSec: attempt.activeSec, runs: attempt.runs, hintsUsed: attempt.hintsUsed });
    if (editor) editor.setReadOnly(true);
    if (answerEl) answerEl.disabled = true;
    for (const b of [runBtn, testBtn, resetBtn, checkBtn, giveUpBtn]) if (b) b.disabled = true;
    renderOutcome(result, await nextNavigation());
  }

  function renderOutcome(result, nav) {
    const label = result === "passed" ? t("task.passed") : result === "gaveUp" ? t("task.gaveUp") : t("task.failed");
    const box = h("section", { class: `outcome ${result}` },
      h("h3", {}, `${result === "passed" ? "✓" : "•"} ${label} · ${fmtDuration(attempt.activeSec)}`),
      isDiagnostic ? null : h("p", { class: "fun" }, randomFrom(t(result === "passed" ? "fun.pass" : "fun.gaveUp"))));
    if (!isDiagnostic) {
      box.append(ruleBox());
      box.append(h("h4", {}, t("task.explanation")), h("p", {}, pick(task, "explanation")));
      const lv = task.levels;
      const solutionShownAsLevel = lv && [lv.middle.code, lv.senior.code].some((c) => c.trim() === task.solution.trim());
      if (!solutionShownAsLevel) box.append(solutionBlock());
      if (lv) box.append(levelsBlock(lv));
      if (task.talk_track?.length) box.append(h("h4", {}, t("task.talk")), h("ul", {}, task.talk_track.map((l) => h("li", {}, l))));
      if (task.followups?.length) box.append(h("h4", {}, t("task.followups")), h("ul", {}, task.followups.map((l) => h("li", {}, l))));
    }
    actions.append(h("a", { class: "btn btn-primary big", href: nav.hash }, nav.label));
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
    if (finished || !editor) return;
    if (!window.confirm(t("task.resetConfirm"))) return;
    editor.setDoc(v.starter);
    ctx.store.kvDelete(draftKey(draftId));
    editor.focus();
  }

  return () => {
    clearInterval(timer);
    offTheme();
    offSettings();
    if (!finished && attempt.runs > 0) {
      attempt.result = "left";
      attempt.endedAt = now();
      attempt.code = currentCode();
      attempt.errors = errorsArray();
      ctx.store.putAttempt(attempt);
    }
    editor?.destroy();
  };
}
