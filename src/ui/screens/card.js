import { h } from "../dom.js";
import { markSessionStep, markCardSeen } from "../../core/state.js";

/**
 * The card itself (title, chapter story, intro, concept chips, snippets, gotchas, interview phrase).
 * Shared by the card screen and the in-task overlay; `kicker` is the small line above the title.
 */
export function renderCardBody(ctx, mod, { kicker = null } = {}) {
  const { t, pick, content } = ctx;
  const card = mod.card || {};
  const out = [];
  out.push(h("header", { class: "screen-head" },
    kicker ? h("p", { class: "muted" }, kicker) : null,
    h("h1", {}, pick(mod, "title")),
    mod.chapter_en ? h("section", { class: "story" }, h("h3", {}, `🔥 ${pick(mod, "chapter")}`), h("p", {}, pick(mod, "story"))) : null,
    h("p", { class: "lead" }, pick(card, "intro")),
    h("div", { class: "chips" }, mod.concepts.map((c) => h("span", { class: "chip" }, content.concepts[c]?.[ctx.settings.lang] || content.concepts[c]?.en || c))),
  ));

  const snippets = h("div", { class: "snippets" });
  for (const sn of card.snippets || []) {
    snippets.append(h("section", { class: "snippet card" },
      h("h3", {}, pick(sn, "title")),
      h("pre", { class: "code" }, h("code", {}, sn.code.replace(/\n$/, ""))),
      h("p", { class: "note" }, pick(sn, "note")),
    ));
  }
  out.push(snippets);

  const gotchas = pick(card, "gotchas");
  if (Array.isArray(gotchas) && gotchas.length) {
    out.push(h("section", { class: "card warn" }, h("h3", {}, t("card.gotchas")), h("ul", {}, gotchas.map((g) => h("li", {}, g)))));
  }
  if (card.phrase_en) {
    out.push(h("section", { class: "card phrase" }, h("h3", {}, t("card.phrase")), h("p", { class: "quote" }, `“${card.phrase_en}”`)));
  }
  return out;
}

export async function renderCard(ctx, root, param, query) {
  const { t, content } = ctx;
  const mod = content.modules.find((m) => m.id === param);
  if (!mod) { root.append(h("p", { class: "muted" }, t("task.notFound"))); return; }
  const inSession = query.date && query.step !== undefined && query.step !== "";

  root.append(...renderCardBody(ctx, mod, { kicker: `${t("card.title")} · L${mod.level}` }));

  const actions = h("div", { class: "row" });
  if (inSession) {
    actions.append(h("button", { class: "btn btn-primary big", onclick: async () => {
      await markSessionStep(ctx.store, query.date, Number(query.step), { status: "done", result: "passed" });
      await markCardSeen(ctx.store, mod.id);
      ctx.logEvent("card", mod.id, {});
      ctx.navigate("#/session");
    } }, t("card.done")));
  } else {
    actions.append(h("button", { class: "btn", onclick: async () => { await markCardSeen(ctx.store, mod.id); ctx.logEvent("card", mod.id, {}); ctx.navigate("#/map"); } }, t("card.close")));
  }
  root.append(actions);
}
