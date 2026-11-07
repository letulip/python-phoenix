/** The idiom gym: families of short drills with spaced repetition. `#/gym` lists the families, `#/gym/round` runs the round of the day. */
import { h } from "../dom.js";
import { buildHash } from "../router.js";
import { randomFrom } from "../i18n.js";
import { todayKey } from "../../core/progress.js";
import { buildRound, familySummary, gymCounts, ROUND_SIZE } from "../../core/srs.js";
import { loadRound, saveRound, loadSrs, archiveRound } from "../../core/state.js";

export function gymStepHash(step, index) {
  return buildHash("task", step.id, { mode: "gym", step: index, variant: step.variant });
}

export function familyOf(content, id) {
  return (content.gym?.families || []).find((f) => f.id === id) || null;
}

export async function renderGym(ctx, root, param, query) {
  if (param === "round") return renderRound(ctx, root, query);
  return renderOverview(ctx, root);
}

async function renderOverview(ctx, root) {
  const { t, pick, content } = ctx;
  const srs = await loadSrs(ctx.store);
  const today = todayKey();
  const counts = gymCounts(content, srs, today);
  const summary = familySummary(content, srs, today);
  const round = await loadRound(ctx.store);
  const pending = !!round && round.steps.some((s) => s.status === "pending");

  root.append(h("header", { class: "screen-head" },
    h("h1", {}, t("gym.title")),
    h("p", { class: "lead" }, t("gym.intro")),
    h("p", { class: "muted" }, t("gym.counts", { due: counts.due + counts.fresh, mastered: counts.mastered, total: counts.total })),
    h("div", { class: "row" },
      h("a", { class: "btn btn-primary big", href: "#/gym/round" }, pending ? t("gym.round.continue") : t("gym.round.start", { n: ROUND_SIZE }))),
  ));

  for (const tier of [1, 2]) {
    const fams = summary.filter((f) => f.tier === tier);
    if (!fams.length) continue;
    root.append(h("h2", { class: "tier-title" }, t(`gym.tier${tier}`)));
    for (const f of fams) {
      const family = familyOf(content, f.id);
      const pct = Math.round(f.mastery * 100);
      root.append(h("section", { class: "module family" },
        h("header", { class: "module-head" },
          h("h3", {}, pick(family, "title")),
          h("span", { class: "muted" }, t("gym.family.stats", { mastered: f.mastered, total: f.total, due: f.due + f.fresh })),
          h("a", { class: "btn btn-ghost small", href: buildHash("gym", "round", { family: f.id }) }, t("gym.family.train")),
        ),
        h("p", { class: "rule" }, pick(family, "rule")),
        h("div", { class: "progress-bar" }, h("div", { class: "progress-fill", style: `width:${pct}%` })),
        h("ul", { class: "drill-list" }, family.drills.map((id) => {
          const d = content.tasks[id];
          const s = srs[id];
          return h("li", { class: "drill" },
            h("span", { class: `badge small type-${d.type}` }, t(`task.type.${d.type}`)),
            h("a", { href: buildHash("task", id, { mode: "free", variant: s ? s.seen % (d.variants?.length || 1) : 0 }) }, d.title),
            h("span", { class: "muted" }, s ? t("gym.box", { box: s.box, due: s.due }) : t("gym.newCard")));
        })),
      ));
    }
  }
}

async function renderRound(ctx, root, query) {
  const { t, pick, content } = ctx;
  const today = todayKey();
  let round = await loadRound(ctx.store);
  const wantFamily = query.family || null;
  const finished = !!round && !round.steps.some((s) => s.status === "pending");

  if (!round || wantFamily || (finished && query.new)) {
    const srs = await loadSrs(ctx.store);
    round = buildRound({ content, srs, today, familyId: wantFamily });
    round.startedAt = new Date().toISOString();
    await saveRound(ctx.store, round);
    if (wantFamily || query.new) { ctx.navigate("#/gym/round"); return; }
  }

  const nextIndex = round.steps.findIndex((s) => s.status === "pending");
  const allDone = nextIndex === -1;
  const family = round.familyId ? familyOf(content, round.familyId) : null;

  root.append(h("header", { class: "screen-head" },
    h("h1", {}, t("gym.round.title")),
    h("p", { class: "muted" }, `${round.date}${family ? ` · ${pick(family, "title")}` : ""}`),
  ));

  if (!round.steps.length) {
    root.append(h("p", {}, t("gym.round.empty")), h("a", { class: "btn", href: "#/gym" }, t("gym.round.toGym")));
    return;
  }

  const list = h("ol", { class: "steps" });
  round.steps.forEach((step, i) => {
    const task = content.tasks[step.id];
    const fam = familyOf(content, step.family);
    const isCurrent = i === nextIndex;
    const stateClass = step.status === "done" ? (step.result === "passed" ? "done" : "done-fail") : isCurrent ? "current" : "pending";
    const href = step.status === "done" ? buildHash("task", step.id, { mode: "free", variant: step.variant }) : gymStepHash(step, i);
    list.append(h("li", { class: `step ${stateClass}` }, h("a", { href, class: "step-link" },
      h("span", { class: "step-icon" }, step.status === "done" ? (step.result === "passed" ? "✓" : "✗") : isCurrent ? "▶" : String(i + 1)),
      h("span", { class: "step-role" }, t(`task.type.${task.type}`)),
      h("span", { class: "step-title" }, `${task.title}`, h("span", { class: "muted" }, ` · ${pick(fam, "title")}`)),
      h("span", { class: "muted" }, `${task.minutes} ${t("common.min")}`),
    )));
  });
  root.append(list);

  if (!allDone) {
    const started = round.steps.some((s) => s.status !== "pending");
    root.append(h("div", { class: "row" },
      h("a", { class: "btn btn-primary big", href: gymStepHash(round.steps[nextIndex], nextIndex) }, started ? t("gym.round.continue") : t("gym.round.begin"))));
    return;
  }

  if (!round.recorded) {
    round.recorded = true;
    round.finishedAt = new Date().toISOString();
    await saveRound(ctx.store, round);
    await archiveRound(ctx.store, {
      date: round.date, startedAt: round.startedAt, finishedAt: round.finishedAt, familyId: round.familyId,
      items: round.steps.length, passed: round.steps.filter((s) => s.result === "passed").length,
    });
  }
  const srs = await loadSrs(ctx.store);
  const passed = round.steps.filter((s) => s.result === "passed").length;
  let firstTry = 0;
  for (const step of round.steps) {
    if (step.result !== "passed" || !step.attemptId) continue;
    const a = await ctx.store.getAttempt(step.attemptId);
    if (a && (a.runs || 0) <= 1) firstTry += 1;
  }
  const touched = [...new Set(round.steps.map((s) => s.family))];
  const nextDue = round.steps.map((s) => srs[s.id]?.due).filter(Boolean).sort()[0] || "–";
  root.append(h("section", { class: "card accent" },
    h("h2", {}, t("gym.round.done.title")),
    h("p", { class: "fun" }, randomFrom(t(passed === round.steps.length ? "fun.pass" : "fun.fail"))),
    h("p", {}, t("gym.round.done.text", { passed, items: round.steps.length, firstTry, next: nextDue })),
    h("p", { class: "muted" }, touched.map((id) => pick(familyOf(content, id), "title")).join(" · ")),
    h("div", { class: "row" },
      h("a", { class: "btn btn-primary", href: buildHash("gym", "round", { new: 1 }) }, t("gym.round.again")),
      h("a", { class: "btn btn-ghost", href: "#/gym" }, t("gym.round.toGym")),
      h("a", { class: "btn btn-ghost", href: "#/home" }, t("session.home"))),
  ));
}
