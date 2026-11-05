import { h, WORLD_ICON } from "../dom.js";
import { buildHash } from "../router.js";
import { computeModuleStatuses, indexAttempts, sortedModules } from "../../core/progress.js";

export async function renderMap(ctx, root) {
  const { t, pick, content } = ctx;
  const attempts = await ctx.store.getAttempts();
  const byTask = indexAttempts(attempts);
  const { modules: statuses } = computeModuleStatuses(content, attempts, ctx.profile);

  root.append(h("header", { class: "screen-head" }, h("h1", {}, t("map.title"))));

  for (const mod of sortedModules(content)) {
    const st = statuses[mod.id];
    const pct = st.total ? Math.round((st.passed / st.total) * 100) : 0;
    root.append(h("section", { class: `module module-${st.status}` },
      h("header", { class: "module-head" },
        h("h2", {}, `L${mod.level} · ${pick(mod, "title")}`),
        h("span", { class: `badge status-${st.status}` }, t(`map.status.${st.status}`)),
        h("span", { class: "muted" }, `${st.passed}/${st.total}`),
        h("a", { class: "btn btn-ghost small", href: buildHash("card", mod.id) }, t("map.card")),
      ),
      mod.chapter_en ? h("p", { class: "chapter muted" }, `🔥 ${pick(mod, "chapter")}`) : null,
      st.status === "done" && mod.story_done_en ? h("p", { class: "story-line" }, pick(mod, "story_done")) : null,
      h("div", { class: "progress-bar" }, h("div", { class: "progress-fill", style: `width:${pct}%` })),
      h("ol", { class: "exercise-list" }, mod.exercises.map((id) => {
        const task = content.tasks[id];
        const info = byTask.get(id);
        const state = info?.passed ? "passed" : info ? "tried" : "new";
        return h("li", { class: `exercise ${state}` },
          h("a", { href: buildHash("task", id, { mode: "free" }) },
            h("span", { class: "ex-icon" }, state === "passed" ? "✓" : state === "tried" ? "•" : "○"),
            h("span", { class: `badge small type-${task.type}` }, t(`task.type.${task.type}`)),
            h("span", { class: "ex-title" }, task.title),
            h("span", { class: "muted ex-meta" }, `${WORLD_ICON[task.world] || ""} ${task.minutes} ${t("common.min")}`),
          ));
      })),
    ));
  }
}
