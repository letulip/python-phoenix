import { h } from "../dom.js";
import { buildHash } from "../router.js";
import { randomFrom } from "../i18n.js";
import { buildSession, seededRandom, todayKey, computeStreak } from "../../core/progress.js";
import { loadSession, saveSession , loadCardsSeen } from "../../core/state.js";

export function stepHash(step, index, date) {
  return step.kind === "card"
    ? buildHash("card", step.id, { date, step: index })
    : buildHash("task", step.id, { mode: step.role, date, step: index });
}

async function finalize(ctx, session) {
  const sessions = await ctx.store.kvGet("sessions", []);
  const attempts = [];
  for (const step of session.steps) if (step.attemptId) attempts.push(await ctx.store.getAttempt(step.attemptId));
  const real = attempts.filter(Boolean);
  const activeSec = real.reduce((s, a) => s + (a.activeSec || 0), 0);
  const summary = {
    date: session.date, minutes: Math.round(activeSec / 60), items: session.steps.length,
    passed: real.filter((a) => a.result === "passed").length,
    newTasks: session.steps.filter((s) => s.role === "lesson" && s.result === "passed").length,
    reviews: session.steps.filter((s) => s.role === "review" && s.status === "done").length,
    hints: real.reduce((s, a) => s + (a.hintsUsed || 0), 0),
    errors: real.reduce((s, a) => s + (a.errors || []).reduce((x, e) => x + e.count, 0), 0),
    activeSec,
  };
  if (!session.recorded) {
    const others = sessions.filter((s) => s.date !== session.date);
    summary.streakDay = computeStreak([...others, summary], session.date);
    await ctx.store.kvSet("sessions", [...others, { date: summary.date, minutes: summary.minutes, items: summary.items, newTasks: summary.newTasks, reviews: summary.reviews, streakDay: summary.streakDay }]);
    session.recorded = true;
    session.finishedAt = new Date().toISOString();
    await saveSession(ctx.store, session);
  }
  return summary;
}

export async function renderSession(ctx, root) {
  const { t, pick, content } = ctx;
  const date = todayKey();
  let session = await loadSession(ctx.store, date);
  if (!session) {
    const attempts = await ctx.store.getAttempts();
    session = buildSession({ content, attempts, profile: ctx.profile, settings: ctx.settings, date, random: seededRandom(date), cardsSeen: await loadCardsSeen(ctx.store) });
    session.startedAt = new Date().toISOString();
    await saveSession(ctx.store, session);
  }
  const mod = session.moduleId ? content.modules.find((m) => m.id === session.moduleId) : null;
  const nextIndex = session.steps.findIndex((s) => s.status === "pending");
  const allDone = nextIndex === -1;

  root.append(h("header", { class: "screen-head" },
    h("h1", {}, t("session.title")),
    h("p", { class: "muted" }, `${date}${mod ? ` · L${mod.level} · ${pick(mod, "title")}` : ""}`),
  ));

  if (!session.steps.length) {
    root.append(h("p", {}, t("session.empty")), h("a", { class: "btn", href: "#/map" }, t("home.map")));
    return;
  }

  const list = h("ol", { class: "steps" });
  session.steps.forEach((step, i) => {
    const task = step.kind === "exercise" ? content.tasks[step.id] : null;
    const title = step.kind === "card" ? t("session.step.card", { module: pick(content.modules.find((m) => m.id === step.id), "title") }) : task?.title || step.id;
    const minutes = step.kind === "card" ? 3 : task?.minutes || 0;
    const isCurrent = i === nextIndex;
    const stateClass = step.status === "done" ? (step.result === "passed" || step.kind === "card" ? "done" : "done-fail") : isCurrent ? "current" : "pending";
    const link = h("a", { href: stepHash(step, i, date), class: `step-link` },
      h("span", { class: "step-icon" }, step.status === "done" ? (step.result === "passed" || step.kind === "card" ? "✓" : "✗") : isCurrent ? "▶" : String(i + 1)),
      h("span", { class: "step-role" }, t(`session.role.${step.role}`)),
      h("span", { class: "step-title" }, title),
      h("span", { class: "muted" }, `${minutes} ${t("common.min")}`),
    );
    if (step.status === "done") link.setAttribute("href", step.kind === "card" ? buildHash("card", step.id) : buildHash("task", step.id, { mode: "free" }));
    list.append(h("li", { class: `step ${stateClass}` }, link));
  });
  root.append(list);

  if (!allDone) {
    const started = session.steps.some((s) => s.status !== "pending");
    root.append(h("div", { class: "row" },
      h("a", { class: "btn btn-primary big", href: stepHash(session.steps[nextIndex], nextIndex, date) }, started ? t("session.continue") : t("session.begin"))));
    return;
  }

  const summary = await finalize(ctx, session);
  root.append(h("section", { class: "card accent" },
    h("h2", {}, t("session.done.title")),
    h("p", { class: "fun" }, randomFrom(t("fun.pass"))),
    h("p", {}, t("session.done.text", { items: summary.items, minutes: summary.minutes, passed: summary.passed })),
    h("p", { class: "muted" }, `${t("session.done.hints", { n: summary.hints })} · ${summary.errors ? t("session.done.errors", { n: summary.errors }) : t("session.done.noErrors")}`),
    h("div", { class: "row" },
      h("a", { class: "btn btn-primary", href: "#/home" }, t("session.home")),
      h("a", { class: "btn btn-ghost", href: "#/progress" }, t("home.progress"))),
  ));
}
