/** Hash router: "#/task/l0.functions.cat-years?mode=lesson&date=2026-11-05&step=2". */

export function parseHash(hash) {
  const raw = (hash || "").replace(/^#\/?/, "");
  const [pathPart, queryPart = ""] = raw.split("?");
  const segments = pathPart.split("/").filter(Boolean);
  const route = segments[0] || "home";
  const param = segments.length > 1 ? decodeURIComponent(segments.slice(1).join("/")) : null;
  const query = {};
  for (const pair of queryPart.split("&")) {
    if (!pair) continue;
    const [k, v = ""] = pair.split("=");
    query[decodeURIComponent(k)] = decodeURIComponent(v);
  }
  return { route, param, query };
}

export function buildHash(route, param = null, query = {}) {
  let hash = `#/${route}`;
  if (param) hash += `/${encodeURIComponent(param)}`;
  const q = Object.entries(query).filter(([, v]) => v != null && v !== "")
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join("&");
  return q ? `${hash}?${q}` : hash;
}

export function createRouter({ root, ctx, routes, notFound }) {
  let cleanup = null;
  let rendering = 0;

  async function render() {
    const { route, param, query } = parseHash(location.hash);
    const screen = routes[route] || notFound;
    const token = ++rendering;
    if (typeof cleanup === "function") { try { cleanup(); } catch (err) { console.error(err); } }
    cleanup = null;
    root.replaceChildren();
    root.dataset.route = route;
    document.querySelectorAll("[data-nav]").forEach((a) => a.classList.toggle("active", a.dataset.nav === route));
    try {
      const result = await screen(ctx, root, param, query);
      if (token === rendering && typeof result === "function") cleanup = result;
    } catch (err) {
      console.error(err);
      root.replaceChildren();
      const p = document.createElement("p");
      p.className = "error";
      p.textContent = `Screen error: ${err.message}`;
      root.append(p);
    }
    window.scrollTo(0, 0);
  }

  return {
    start() {
      window.addEventListener("hashchange", render);
      if (!location.hash) location.hash = "#/home";
      else render();
    },
    navigate(hash) {
      if (location.hash === hash) render();
      else location.hash = hash;
    },
    rerender: render,
  };
}
