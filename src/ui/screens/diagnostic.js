import { h } from "../dom.js";
import { buildHash } from "../router.js";
import { sortedModules, evaluatePlacement } from "../../core/progress.js";
import { loadDiagnostic, saveDiagnostic, clearDiagnostic } from "../../core/state.js";

export async function renderDiagnostic(ctx, root) {
  const { t, pick, content } = ctx;
  const queue = sortedModules(content).flatMap((m) => m.diagnostic);
  let state = await loadDiagnostic(ctx.store);

  if (state && state.index < state.queue.length) {
    root.append(h("p", { class: "muted" }, t("diag.progress", { i: state.index + 1, n: state.queue.length })));
    ctx.navigate(buildHash("task", state.queue[state.index], { mode: "diagnostic" }));
    return;
  }

  if (state && state.index >= state.queue.length) {
    const placement = evaluatePlacement(content, state.results || []);
    ctx.profile.placement = placement;
    await ctx.saveProfile();
    await clearDiagnostic(ctx.store);
    const knownTitles = placement.known.map((id) => pick(content.modules.find((m) => m.id === id), "title"));
    const startMod = content.modules.find((m) => m.id === placement.startModule);
    root.append(h("section", { class: "card accent" },
      h("h1", {}, t("diag.result.title")),
      h("p", {}, knownTitles.length ? t("diag.result.known", { modules: knownTitles.join(", ") }) : t("diag.result.none")),
      startMod ? h("p", {}, t("diag.result.start", { module: pick(startMod, "title") })) : null,
      h("ul", { class: "diag-results" }, (state.results || []).map((r) => {
        const task = content.tasks[r.taskId];
        return h("li", { class: r.passed ? "pass" : "fail" }, `${r.passed ? "✓" : "✗"} ${task?.title || r.taskId}`);
      })),
      h("div", { class: "row" }, h("a", { class: "btn btn-primary", href: "#/home" }, t("diag.home"))),
    ));
    return;
  }

  root.append(h("section", { class: "card" },
    h("h1", {}, t("diag.title")),
    h("p", {}, t("diag.intro", { n: queue.length })),
    h("div", { class: "row" },
      h("button", { class: "btn btn-primary big", onclick: async () => {
        state = { startedAt: new Date().toISOString(), queue, index: 0, results: [] };
        await saveDiagnostic(ctx.store, state);
        ctx.logEvent("diagnostic-start", null, { n: queue.length });
        ctx.navigate(buildHash("task", queue[0], { mode: "diagnostic" }));
      } }, t("diag.start")),
      h("a", { class: "btn btn-ghost", href: "#/home" }, t("common.back")),
    ),
  ));
}
