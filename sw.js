/* Python Phoenix service worker.
 * Same-origin files: network first, cache fallback (so deploys show up on the next load, and the
 * app still opens offline). Pyodide from the CDN: cache first (15 MB that never changes per version). */
const VERSION = "0.1.0";
const SHELL_CACHE = `pp-shell-${VERSION}`;
const PYODIDE_CACHE = "pp-pyodide-314.0.7";
const CDN_PREFIX = "https://cdn.jsdelivr.net/pyodide/";
const SHELL = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./manifest.json",
  "./content/tasks.json",
  "./vendor/codemirror.js",
  "./icons/icon.svg",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./src/core/diff.js",
  "./src/core/export.js",
  "./src/core/progress.js",
  "./src/core/state.js",
  "./src/core/store.js",
  "./src/editor/editor.js",
  "./src/runner/client.js",
  "./src/runner/runner.py",
  "./src/runner/worker.js",
  "./src/ui/dom.js",
  "./src/ui/i18n.js",
  "./src/ui/mismatch.js",
  "./src/ui/router.js",
  "./src/ui/screens/card.js",
  "./src/ui/screens/diagnostic.js",
  "./src/ui/screens/home.js",
  "./src/ui/screens/map.js",
  "./src/ui/screens/progress.js",
  "./src/ui/screens/session.js",
  "./src/ui/screens/settings.js",
  "./src/ui/screens/task.js",
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL_CACHE);
    await Promise.allSettled(SHELL.map((url) => cache.add(url)));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== SHELL_CACHE && k !== PYODIDE_CACHE).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(request);
  if (hit) return hit;
  const response = await fetch(request);
  if (response.ok) cache.put(request, response.clone());
  return response;
}

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const hit = await cache.match(request, { ignoreSearch: true });
    if (hit) return hit;
    if (request.mode === "navigate") {
      const index = await cache.match("./index.html");
      if (index) return index;
    }
    throw err;
  }
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  if (request.url.startsWith(CDN_PREFIX)) { event.respondWith(cacheFirst(request, PYODIDE_CACHE)); return; }
  if (new URL(request.url).origin === self.location.origin) event.respondWith(networkFirst(request, SHELL_CACHE));
});
