import { h } from "../dom.js";
import { buildHash } from "../router.js";
import { computeModuleStatuses, computeStreak, todayKey, buildSession, seededRandom, sessionMinutes, sortedModules } from "../../core/progress.js";
import { loadSession , loadCardsSeen } from "../../core/state.js";

export async function renderHome(ctx, root) {
  const { t, pick, content } = ctx;
  const attempts = await ctx.store.getAttempts();
  const sessions = await ctx.store.kvGet("sessions", []);
  const { modules: statuses, currentModule } = computeModuleStatuses(content, attempts, ctx.profile);
  const date = todayKey();
  const session = await loadSession(ctx.store, date);
  const streak = computeStreak(sessions, date);
  const passed = Object.values(statuses).reduce((s, m) => s + m.passed, 0);
  const total = Object.values(statuses).reduce((s, m) => s + m.total, 0);
  const diagnosticCount = sortedModules(content).reduce((s, m) => s + m.diagnostic.length, 0);

  root.append(h("section", { class: "hero" },
    h("h1", {}, "Python Phoenix"),
    h("p", { class: "tagline" }, t("home.tagline")),
  ));

  if (!ctx.profile.placement && attempts.length === 0 && diagnosticCount > 0) {
    root.append(h("section", { class: "card accent" },
      h("h2", {}, t("home.placement.title")),
      h("p", {}, t("home.placement.text", { n: diagnosticCount })),
      h("div", { class: "row" },
        h("a", { class: "btn btn-primary", href: "#/diagnostic" }, t("home.placement.start")),
        h("button", { class: "btn btn-ghost", onclick: async () => {
          ctx.profile.placement = { at: new Date().toISOString(), skipped: true, known: [], startModule: currentModule, results: [] };
          await ctx.saveProfile();
          ctx.navigate("#/home");
        } }, t("home.placement.skip")),
      ),
    ));
  }

  const sessionCard = h("section", { class: "card" }, h("h2", {}, t("home.session.title")));
  if (session) {
    const done = session.steps.filter((s) => s.status !== "pending").length;
    if (done === session.steps.length) {
      sessionCard.append(h("p", {}, t("home.session.done")),
        h("a", { class: "btn", href: "#/session" }, t("home.session.open")));
    } else {
      sessionCard.append(h("p", {}, t("home.session.progress", { done, total: session.steps.length })),
        h("a", { class: "btn btn-primary", href: "#/session" }, t("home.session.continue")));
    }
  } else if (currentModule) {
    const preview = buildSession({ content, attempts, profile: ctx.profile, settings: ctx.settings, date, random: seededRandom(date), cardsSeen: await loadCardsSeen(ctx.store) });
    const mod = content.modules.find((m) => m.id === currentModule);
    if (mod.chapter_en) sessionCard.append(h("p", { class: "chapter muted" }, `🔥 ${pick(mod, "chapter")}`));
    sessionCard.append(h("p", {}, t("home.session.new", { module: pick(mod, "title"), minutes: sessionMinutes(content, preview) })),
      h("a", { class: "btn btn-primary", href: "#/session" }, t("home.session.start")));
  } else {
    sessionCard.append(h("p", {}, t("home.allDone")), h("a", { class: "btn", href: "#/map" }, t("home.map")));
  }
  root.append(sessionCard);

  const pyValue = h("div", { class: "stat-value" }, ctx.runtime.python || "…");
  root.append(h("section", { class: "stats-row" },
    h("div", { class: "stat" }, h("div", { class: "stat-value" }, String(streak)), h("div", { class: "stat-label" }, `${t("home.streak")} · ${t("home.days")}`)),
    h("div", { class: "stat" }, h("div", { class: "stat-value" }, `${passed}/${total}`), h("div", { class: "stat-label" }, t("home.passed"))),
    h("div", { class: "stat" }, pyValue, h("div", { class: "stat-label" }, "Python")),
  ));
  const offRuntime = ctx.on("runtime", (rt) => { pyValue.textContent = rt.python || "…"; });

  if (ctx.profile.placement?.startModule && ctx.profile.placement.known?.length) {
    const mod = content.modules.find((m) => m.id === ctx.profile.placement.startModule);
    if (mod) root.append(h("p", { class: "muted" }, t("home.module.start", { module: pick(mod, "title") })));
  }

  root.append(h("div", { class: "row" },
    h("a", { class: "btn btn-ghost", href: buildHash("map") }, t("home.map")),
    h("a", { class: "btn btn-ghost", href: buildHash("progress") }, t("home.progress")),
  ));
  return offRuntime;
}
