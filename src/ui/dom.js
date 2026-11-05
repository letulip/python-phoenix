/** Tiny DOM helpers: no framework, no templates, just elements. */

export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs || {})) {
    if (value == null || value === false) continue;
    if (key === "class") el.className = value;
    else if (key === "style") el.style.cssText = value;
    else if (key === "html") el.innerHTML = value;
    else if (key.startsWith("on") && typeof value === "function") el.addEventListener(key.slice(2).toLowerCase(), value);
    else if (value === true) el.setAttribute(key, "");
    else el.setAttribute(key, String(value));
  }
  for (const child of children.flat(Infinity)) {
    if (child == null || child === false) continue;
    el.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return el;
}

export function clear(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
  return el;
}

export function toast(message, kind = "info", ms = 3200) {
  const host = document.getElementById("toasts");
  if (!host) return;
  const el = h("div", { class: `toast toast-${kind}`, role: "status" }, message);
  host.append(el);
  setTimeout(() => { el.classList.add("toast-out"); setTimeout(() => el.remove(), 300); }, ms);
}

export function fmtDuration(totalSec) {
  const sec = Math.max(0, Math.round(totalSec));
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export function dots(n, max = 5) {
  return "●".repeat(Math.max(0, Math.min(max, n))) + "○".repeat(Math.max(0, max - n));
}

export const WORLD_ICON = { game: "🎮", everyday: "🏠", neutral: "📐", shorts: "🎬", bybit: "📈", tennis: "🎾", oth: "🚙" };

export function isMac() {
  return typeof navigator !== "undefined" && /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || "");
}

export function modKey() { return isMac() ? "⌘" : "Ctrl"; }

export function debounce(fn, ms) {
  let timer = null;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}

/**
 * Modal overlay on top of the current screen (native <dialog>): Esc, the ✕ button and a click on the
 * backdrop close it; the element is removed on close and focus returns to whatever opened it.
 */
export function openDialog({ title, body, closeLabel = "Close", onClose = null }) {
  const opener = document.activeElement;
  const dlg = h("dialog", { class: "overlay" },
    h("div", { class: "overlay-head" },
      h("span", { class: "muted" }, title),
      h("button", { class: "btn btn-ghost small", type: "button", "aria-label": closeLabel, title: closeLabel, onclick: () => dlg.close() }, "✕")),
    h("div", { class: "overlay-body" }, body));
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  dlg.addEventListener("close", () => {
    dlg.remove();
    if (onClose) onClose();
    if (opener && typeof opener.focus === "function") opener.focus();
  });
  document.body.append(dlg);
  dlg.showModal();
  return dlg;
}
