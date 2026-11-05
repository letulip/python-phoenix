import { h, toast, fmtDuration } from "../dom.js";
import { aggregateStats, sortedModules, todayKey } from "../../core/progress.js";
import { buildExport, mergeImport } from "../../core/export.js";

async function collect(ctx) {
  return {
    attempts: await ctx.store.getAttempts(),
    events: await ctx.store.getEvents(),
    sessions: await ctx.store.kvGet("sessions", []),
  };
}

function download(name, text) {
  const blob = new Blob([text], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = h("a", { href: url, download: name });
  document.body.append(a);
  a.click();
  setTimeout(() => { a.remove(); URL.revokeObjectURL(url); }, 500);
}

export async function renderProgress(ctx, root) {
  const { t, content } = ctx;
  const { attempts, events, sessions } = await collect(ctx);
  const stats = aggregateStats(content, attempts);
  const conceptName = (id) => content.concepts[id]?.[ctx.settings.lang] || content.concepts[id]?.en || id;

  const exportJson = () => JSON.stringify(buildExport({ version: ctx.version, profile: ctx.profile, settings: ctx.settings, attempts, events, sessions, content }), null, 1);

  const fileInput = h("input", { type: "file", accept: "application/json,.json", style: "display:none", onchange: async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const imported = JSON.parse(await file.text());
      const merged = mergeImport({ profile: ctx.profile, settings: ctx.settings, attempts, events, sessions }, imported);
      const localIds = new Set(attempts.map((a) => a.id));
      for (const a of merged.attempts) if (!localIds.has(a.id)) await ctx.store.putAttempt(a);
      const localEvents = new Set(events.map((ev) => ev.id));
      for (const ev of merged.events) if (!localEvents.has(ev.id)) await ctx.store.addEvent(ev);
      await ctx.store.kvSet("sessions", merged.sessions);
      ctx.profile = merged.profile; await ctx.saveProfile();
      Object.assign(ctx.settings, merged.settings); await ctx.saveSettings();
      toast(t("progress.imported", { attempts: merged.added.attempts }), "ok");
      ctx.navigate("#/progress");
    } catch (err) {
      toast(t("progress.importError", { message: err.message }), "warn", 6000);
    }
  } });

  root.append(h("header", { class: "screen-head" },
    h("h1", {}, t("progress.title")),
    h("p", { class: "muted" }, t("progress.summary", { passed: stats.passedExercises, total: stats.totalExercises, attempts: stats.attempts, noHint: Math.round(stats.noHintRate * 100) })),
    h("div", { class: "row" },
      h("button", { class: "btn btn-primary", onclick: () => download(`python-phoenix-progress-${todayKey()}.json`, exportJson()) }, t("progress.export")),
      h("button", { class: "btn", onclick: async () => { try { await navigator.clipboard.writeText(exportJson()); toast(t("progress.copied"), "ok"); } catch (err) { toast(err.message, "warn"); } } }, t("progress.copy")),
      h("button", { class: "btn", onclick: () => fileInput.click() }, t("progress.import")), fileInput,
      h("button", { class: "btn btn-ghost danger", onclick: async () => {
        if (!window.confirm(t("progress.wipeConfirm"))) return;
        await ctx.store.wipe();
        location.reload();
      } }, t("progress.wipe")),
    ),
  ));

  if (!attempts.length) { root.append(h("p", {}, t("progress.noData"))); return; }

  root.append(h("section", { class: "card" }, h("h2", {}, t("progress.modules")),
    sortedModules(content).map((mod) => {
      const m = stats.byModule[mod.id];
      const pct = m.total ? Math.round((m.passed / m.total) * 100) : 0;
      return h("div", { class: "module-row" }, h("span", {}, `L${mod.level} · ${ctx.pick(mod, "title")}`), h("div", { class: "progress-bar" }, h("div", { class: "progress-fill", style: `width:${pct}%` })), h("span", { class: "muted" }, `${m.passed}/${m.total}`));
    })));

  root.append(h("section", { class: "card" }, h("h2", {}, t("progress.concepts")),
    h("table", { class: "table" },
      h("thead", {}, h("tr", {}, h("th", {}, t("progress.col.concept")), h("th", {}, t("progress.col.attempts")), h("th", {}, t("progress.col.pass")), h("th", {}, t("progress.col.hints")), h("th", {}, t("progress.col.median")))),
      h("tbody", {}, stats.byConcept.map((c) => h("tr", { class: c.passRate < 0.5 ? "weak" : "" },
        h("td", {}, conceptName(c.id)), h("td", {}, String(c.attempts)), h("td", {}, `${Math.round(c.passRate * 100)}%`), h("td", {}, c.hintsAvg.toFixed(1)), h("td", {}, c.medianSec == null ? "–" : fmtDuration(c.medianSec))))))));

  root.append(h("section", { class: "card" }, h("h2", {}, t("progress.errors")),
    stats.errors.length ? h("ul", { class: "error-list" }, stats.errors.map((e) => h("li", {}, h("code", {}, e.type), ` × ${e.count}`))) : h("p", { class: "muted" }, t("progress.noErrors"))));

  root.append(h("section", { class: "card" }, h("h2", {}, t("progress.types")),
    h("table", { class: "table" },
      h("thead", {}, h("tr", {}, h("th", {}, t("progress.col.type")), h("th", {}, t("progress.col.attempts")), h("th", {}, t("progress.col.pass")), h("th", {}, t("progress.col.median")))),
      h("tbody", {}, Object.entries(stats.byType).map(([type, s]) => h("tr", {}, h("td", {}, t(`task.type.${type}`)), h("td", {}, String(s.attempts)), h("td", {}, String(s.passed)), h("td", {}, s.medianSec == null ? "–" : fmtDuration(s.medianSec))))))));

  if (sessions.length) {
    root.append(h("section", { class: "card" }, h("h2", {}, t("progress.sessions")),
      h("table", { class: "table" },
        h("thead", {}, h("tr", {}, h("th", {}, t("progress.col.date")), h("th", {}, t("progress.col.minutes")), h("th", {}, t("progress.col.items")))),
        h("tbody", {}, [...sessions].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 14).map((s) => h("tr", {}, h("td", {}, s.date), h("td", {}, String(s.minutes)), h("td", {}, String(s.items))))))));
  }
}
