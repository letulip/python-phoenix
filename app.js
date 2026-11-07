import { Store, uuid } from "./src/core/store.js";
import { Runner } from "./src/runner/client.js";
import { makeT, makePick } from "./src/ui/i18n.js";
import { createRouter, buildHash, parseHash } from "./src/ui/router.js";
import { h, clear, toast } from "./src/ui/dom.js";
import { renderHome } from "./src/ui/screens/home.js";
import { renderSession } from "./src/ui/screens/session.js";
import { renderCard } from "./src/ui/screens/card.js";
import { renderTask } from "./src/ui/screens/task.js";
import { renderMap } from "./src/ui/screens/map.js";
import { renderProgress } from "./src/ui/screens/progress.js";
import { renderSettings } from "./src/ui/screens/settings.js";
import { renderDiagnostic } from "./src/ui/screens/diagnostic.js";
import { renderGym } from "./src/ui/screens/gym.js";

export const APP_VERSION = "0.1.0";
export const DEFAULT_SETTINGS = { lang: "ru", sessionMinutes: 30, pasteInLesson: true, coderpad: false, closeBrackets: true, theme: "auto" };

function createBus() {
  const listeners = new Map();
  return {
    on(event, fn) {
      if (!listeners.has(event)) listeners.set(event, new Set());
      listeners.get(event).add(fn);
      return () => listeners.get(event)?.delete(fn);
    },
    emit(event, data) { for (const fn of listeners.get(event) || []) { try { fn(data); } catch (err) { console.error(err); } } },
  };
}

export function isDark(settings) {
  if (settings.theme === "dark") return true;
  if (settings.theme === "light") return false;
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

export function applyTheme(settings) {
  const rootEl = document.documentElement;
  if (settings.theme === "auto") delete rootEl.dataset.theme;
  else rootEl.dataset.theme = settings.theme;
  rootEl.lang = settings.lang;
}

const NAV = [["home", "nav.today"], ["map", "nav.map"], ["gym", "nav.gym"], ["progress", "nav.progress"], ["settings", "nav.settings"]];

function renderNav(ctx) {
  const nav = document.getElementById("nav");
  const current = parseHash(location.hash).route;
  clear(nav);
  for (const [route, key] of NAV) {
    nav.append(h("a", { href: `#/${route}`, "data-nav": route, class: current === route ? "active" : "" }, ctx.t(key)));
  }
}

function renderRuntime(ctx) {
  const el = document.getElementById("runtime");
  const { status, python, message } = ctx.runtime;
  el.dataset.status = status;
  el.textContent = ctx.t(`runtime.${status}`, { python: python || "", message: message || "" });
}

function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  if (location.search.includes("nosw")) return; // debugging: ?nosw skips the service worker
  navigator.serviceWorker.register("./sw.js").catch((err) => console.warn("service worker:", err.message));
}

async function main() {
  const root = document.getElementById("app");
  const store = await Store.open();
  const response = await fetch("./content/tasks.json", { cache: "no-cache" });
  if (!response.ok) throw new Error(`content/tasks.json: HTTP ${response.status}`);
  const content = await response.json();

  const savedSettings = await store.kvGet("settings", null);
  const settings = { ...DEFAULT_SETTINGS, ...(savedSettings || {}) };
  let profile = await store.kvGet("profile", null);
  if (!profile) {
    profile = { startedAt: new Date().toISOString(), placement: null };
    await store.kvSet("profile", profile);
  }

  const bus = createBus();
  let router = null;
  const ctx = {
    version: APP_VERSION, content, store, settings, profile, runner: null,
    runtime: { status: "idle", python: null },
    t: makeT(() => ctx.settings.lang),
    pick: makePick(() => ctx.settings.lang),
    on: bus.on, emit: bus.emit, toast, buildHash,
    navigate: (hash) => router.navigate(hash),
    isDark: () => isDark(ctx.settings),
    async saveSettings() { await store.kvSet("settings", ctx.settings); applyTheme(ctx.settings); renderNav(ctx); renderRuntime(ctx); bus.emit("settings", ctx.settings); },
    async saveProfile() { await store.kvSet("profile", ctx.profile); },
    async logEvent(k, taskId, data = {}) { try { await store.addEvent({ id: uuid(), t: new Date().toISOString(), k, taskId, data }); } catch (err) { console.warn(err); } },
  };
  applyTheme(settings);

  ctx.runner = new Runner({
    onStatus: (status, extra) => { ctx.runtime = { status, ...extra }; renderRuntime(ctx); bus.emit("runtime", ctx.runtime); },
  });
  ctx.runner.start().catch((err) => console.error("runner:", err));

  router = createRouter({
    root, ctx, notFound: renderHome,
    routes: { home: renderHome, session: renderSession, card: renderCard, task: renderTask, map: renderMap, progress: renderProgress, settings: renderSettings, diagnostic: renderDiagnostic, gym: renderGym },
  });
  renderNav(ctx);
  renderRuntime(ctx);
  document.getElementById("version").textContent = `v${APP_VERSION}`;
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => bus.emit("theme"));
  window.addEventListener("hashchange", () => renderNav(ctx));
  router.start();
  registerServiceWorker();
  window.__phoenix = ctx; // for debugging in the console
}

main().catch((err) => {
  console.error(err);
  const root = document.getElementById("app");
  root.textContent = `Failed to start: ${err.message}`;
});
