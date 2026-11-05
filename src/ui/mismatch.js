/** Expected-versus-got block with the differing characters highlighted and spaces made visible. */
import { h } from "./dom.js";
import { charDiff } from "../core/diff.js";

const DOT = "\u00b7";
const SEP = " \u00b7 ";
const visible = (text) => text.replace(/ /g, DOT);
const joinAll = (list) => (list || []).join(", ");

/** One charDiff per line when both texts have the same number of lines, otherwise one for the whole text. */
function segments(expected, actual) {
  const el = expected.split("\n");
  const al = actual.split("\n");
  if (el.length > 1 && el.length === al.length) return el.map((line, i) => charDiff(line, al[i]));
  return [charDiff(expected, actual)];
}

function textWithMarks(segs, side) {
  const parts = [];
  segs.forEach((s, i) => {
    if (i) parts.push("\n");
    const mid = side === "exp" ? s.aMid : s.bMid;
    const changed = s.aMid.length > 0 || s.bMid.length > 0;
    parts.push(s.prefix, changed ? h("mark", { class: `mismatch-mid ${side}` }, visible(mid)) : null, s.suffix);
  });
  return parts;
}

function row(label, content) {
  return h("div", { class: "mismatch-row" },
    h("span", { class: "mismatch-label" }, label),
    h("code", { class: "mismatch-text" }, content));
}

function notes(t, info, segs) {
  const out = [];
  if (info.etype && info.atype && info.etype !== info.atype) out.push(t("task.mismatch.type", { expected: info.etype, actual: info.atype }));
  if (info.kind === "str") {
    if (info.elen !== info.alen) out.push(t("task.mismatch.len", { expected: info.elen, actual: info.alen }));
    if (segs.length > 1) {
      const n = segs.findIndex((s) => s.aMid || s.bMid);
      if (n >= 0) out.push(t("task.mismatch.line", { n: n + 1 }));
    } else if (info.pos != null) {
      out.push(t("task.mismatch.pos", { pos: info.pos }));
    }
  } else if (info.kind === "seq") {
    if (info.elen !== info.alen) out.push(t("task.mismatch.count", { expected: info.elen, actual: info.alen }));
    if (info.items?.length) {
      out.push(t("task.mismatch.items", { list: info.items.map((it) => it.index).join(", ") }));
      if (info.ndiff > info.items.length) out.push(t("task.mismatch.more", { n: info.ndiff - info.items.length }));
    }
  } else if (info.kind === "dict") {
    if (info.missing?.length) out.push(t("task.mismatch.missing", { keys: joinAll(info.missing) }));
    if (info.extra?.length) out.push(t("task.mismatch.extra", { keys: joinAll(info.extra) }));
    if (info.changed?.length) out.push(t("task.mismatch.changed", { keys: joinAll(info.changed) }));
  } else if (info.kind === "set") {
    if (info.missing?.length) out.push(t("task.mismatch.setMissing", { items: joinAll(info.missing) }));
    if (info.extra?.length) out.push(t("task.mismatch.setExtra", { items: joinAll(info.extra) }));
  }
  if (segs.some((s) => (s.aMid + s.bMid).includes(" "))) out.push(t("task.mismatch.spaces"));
  return out;
}

/** Renders expected/got as two aligned lines: the shared prefix and suffix stay plain, the part that differs is
 *  marked, and spaces inside the mark are drawn as dots. Multi-line text is compared line by line; a list or tuple
 *  is shown whole and then element by element. `info` is the harness's mismatch descriptor and may be empty. */
export function renderMismatch(t, expected, actual, info = {}) {
  const e = String(expected ?? "");
  const a = String(actual ?? "");
  const block = h("div", { class: "mismatch" });
  let segs = [];
  if (info.kind === "seq" && info.items?.length) {
    block.append(row(t("task.wasExpected"), e), row(t("task.got"), a));
  } else {
    segs = segments(e, a);
    block.append(row(t("task.wasExpected"), textWithMarks(segs, "exp")), row(t("task.got"), textWithMarks(segs, "act")));
  }
  const lines = notes(t, info, segs);
  if (lines.length) block.append(h("div", { class: "mismatch-note" }, lines.join(SEP)));
  if (info.kind === "seq") {
    for (const item of info.items || []) {
      const sub = item.kind ? { kind: item.kind, elen: item.elen, alen: item.alen, pos: item.pos } : {};
      block.append(h("div", { class: "mismatch-sub" },
        h("div", { class: "mismatch-note" }, t("task.mismatch.itemLabel", { pos: item.index })),
        renderMismatch(t, item.expected ?? t("task.mismatch.none"), item.actual ?? t("task.mismatch.none"), sub)));
    }
  }
  return block;
}
