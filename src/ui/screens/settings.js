import { h, toast } from "../dom.js";

export async function renderSettings(ctx, root) {
  const { t } = ctx;
  const save = async (patch, rerender = false) => {
    Object.assign(ctx.settings, patch);
    await ctx.saveSettings();
    toast(t("settings.saved"), "ok", 1200);
    if (rerender) ctx.navigate("#/settings");
  };
  const select = (name, options, value, onChange) => h("select", { name, onchange: (e) => onChange(e.target.value) },
    options.map(([v, label]) => h("option", { value: v, selected: String(v) === String(value) }, label)));
  const checkbox = (name, checked, onChange) => h("input", { type: "checkbox", name, checked, onchange: (e) => onChange(e.target.checked) });

  root.append(h("header", { class: "screen-head" }, h("h1", {}, t("settings.title"))));
  root.append(h("section", { class: "card settings" },
    h("label", { class: "setting" }, h("span", {}, t("settings.lang")), select("lang", [["ru", "Русский"], ["en", "English"]], ctx.settings.lang, (v) => save({ lang: v }, true))),
    h("label", { class: "setting" }, h("span", {}, t("settings.sessionMinutes")), select("sessionMinutes", [[20, "20"], [25, "25"], [30, "30"], [45, "45"]], ctx.settings.sessionMinutes, (v) => save({ sessionMinutes: Number(v) }))),
    h("label", { class: "setting" }, h("span", {}, t("settings.theme")), select("theme", [["auto", t("settings.theme.auto")], ["light", t("settings.theme.light")], ["dark", t("settings.theme.dark")]], ctx.settings.theme, (v) => save({ theme: v }))),
    h("label", { class: "setting check" }, checkbox("pasteInLesson", ctx.settings.pasteInLesson, (v) => save({ pasteInLesson: v })), h("span", {}, t("settings.paste"))),
    h("label", { class: "setting check" }, checkbox("coderpad", ctx.settings.coderpad, (v) => save({ coderpad: v })), h("span", {}, t("settings.coderpad"))),
    h("label", { class: "setting check" }, checkbox("closeBrackets", ctx.settings.closeBrackets, (v) => save({ closeBrackets: v })), h("span", {}, t("settings.closeBrackets"))),
  ));
  root.append(h("p", { class: "muted" }, t("settings.version", { version: ctx.version })));
}
