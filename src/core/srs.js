/**
 * Spaced repetition for the idiom gym (pure logic, no DOM, no storage; tested with node --test).
 * Every drill is a card in a Leitner box: a pass moves it up one box and schedules it further away,
 * a fail drops it to box 0 and brings it back tomorrow. Data variants rotate with every attempt,
 * so the same drill never comes back with the same numbers twice in a row.
 */
import { todayKey } from "./progress.js";

export const INTERVALS = [1, 2, 4, 7, 14, 30]; // days until the next review, by box
export const MAX_BOX = INTERVALS.length - 1;
export const MASTERED_BOX = 3;                  // box 3 = survived a week: counts as mastered
export const ROUND_SIZE = 5;

export function addDays(dateKey, days) {
  const d = new Date(`${dateKey}T12:00:00`);
  d.setDate(d.getDate() + days);
  return todayKey(d);
}

export function emptyState() {
  return { box: 0, due: null, seen: 0, passes: 0, fails: 0, lastAt: null, lastResult: null };
}

/** State after an attempt: a pass climbs one box, a fail drops to box 0 and returns tomorrow. */
export function nextState(prev, passed, today, at = null) {
  const s = { ...emptyState(), ...(prev || {}) };
  const box = passed ? Math.min(MAX_BOX, s.box + 1) : 0;
  return {
    box, due: addDays(today, INTERVALS[box]), seen: s.seen + 1,
    passes: s.passes + (passed ? 1 : 0), fails: s.fails + (passed ? 0 : 1),
    lastAt: at || today, lastResult: passed ? "passed" : "failed",
  };
}

/** Variants rotate with the number of attempts made so far. */
export function pickVariant(state, nVariants) {
  return nVariants > 0 ? (state?.seen || 0) % nVariants : 0;
}

export function isDue(state, today) {
  return !state || !state.due || state.due <= today;
}

export function gymCards(content) {
  return (content.gym?.families || []).flatMap((family) => family.drills.map((id) => ({ id, family })));
}

/**
 * Round of the day. Overdue cards first (most overdue first), then new cards interleaved across
 * families (tier 1 before tier 2), then the weakest of the rest. Neighbours are kept in different
 * families when that is possible.
 */
export function buildRound({ content, srs = {}, today = todayKey(), size = ROUND_SIZE, familyId = null }) {
  const cards = gymCards(content)
    .filter((c) => !familyId || c.family.id === familyId)
    .map((c) => ({ ...c, state: srs[c.id] || null, task: content.tasks[c.id] }));
  const famRank = (c) => c.family.tier * 1000 + c.family.order;
  const byOrder = (a, b) => famRank(a) - famRank(b) || a.task.order - b.task.order || a.id.localeCompare(b.id);

  const overdue = cards.filter((c) => c.state && c.state.due && c.state.due <= today)
    .sort((a, b) => a.state.due.localeCompare(b.state.due) || byOrder(a, b));

  // new cards: tier by tier, interleaved across the families of the tier (first drill of each, then second, ...)
  const fresh = [];
  const freshCards = cards.filter((c) => !c.state).sort(byOrder);
  for (const tier of [...new Set(freshCards.map((c) => c.family.tier))].sort()) {
    const byFamily = new Map();
    for (const c of freshCards.filter((c) => c.family.tier === tier)) {
      if (!byFamily.has(c.family.id)) byFamily.set(c.family.id, []);
      byFamily.get(c.family.id).push(c);
    }
    for (let k = 0; ; k++) {
      const row = [...byFamily.values()].map((list) => list[k]).filter(Boolean);
      if (!row.length) break;
      fresh.push(...row);
    }
  }

  const later = cards.filter((c) => c.state && !(c.state.due && c.state.due <= today))
    .sort((a, b) => a.state.box - b.state.box || (a.state.due || "").localeCompare(b.state.due || "") || byOrder(a, b));

  const chosen = [...overdue, ...fresh, ...later].slice(0, size);
  const ordered = [];
  const pool = [...chosen];
  while (pool.length) {
    let idx = pool.findIndex((c) => !ordered.length || c.family.id !== ordered[ordered.length - 1].family.id);
    if (idx < 0) idx = 0;
    ordered.push(pool.splice(idx, 1)[0]);
  }
  const steps = ordered.map((c) => ({
    id: c.id, family: c.family.id, variant: pickVariant(c.state, c.task.variants?.length || 1),
    status: "pending", result: null, attemptId: null,
  }));
  return { date: today, familyId, steps, startedAt: null, finishedAt: null };
}

/** Per-family numbers for the gym screen and the progress table. */
export function familySummary(content, srs = {}, today = todayKey()) {
  return (content.gym?.families || []).map((f) => {
    const states = f.drills.map((id) => srs[id] || null);
    const seen = states.filter(Boolean).length;
    const due = states.filter((s) => s && s.due && s.due <= today).length;
    const fresh = states.filter((s) => !s).length;
    const mastered = states.filter((s) => s && s.box >= MASTERED_BOX).length;
    const boxes = states.reduce((sum, s) => sum + (s?.box || 0), 0);
    const mastery = f.drills.length ? boxes / (f.drills.length * MAX_BOX) : 0;
    const nextDue = states.filter((s) => s?.due).map((s) => s.due).sort()[0] || null;
    const passes = states.reduce((sum, s) => sum + (s?.passes || 0), 0);
    const fails = states.reduce((sum, s) => sum + (s?.fails || 0), 0);
    return { id: f.id, tier: f.tier, total: f.drills.length, seen, fresh, due, mastered, mastery, nextDue, passes, fails };
  });
}

export function gymCounts(content, srs = {}, today = todayKey()) {
  const summary = familySummary(content, srs, today);
  const sum = (key) => summary.reduce((s, f) => s + f[key], 0);
  return { total: sum("total"), seen: sum("seen"), fresh: sum("fresh"), due: sum("due"), mastered: sum("mastered") };
}

/** Merge two srs maps (import): per drill, the state with the later attempt wins. */
export function mergeSrs(local = {}, imported = {}) {
  const out = { ...local };
  for (const [id, state] of Object.entries(imported || {})) {
    if (!state || typeof state !== "object") continue;
    const cur = out[id];
    if (!cur || String(state.lastAt || "") > String(cur.lastAt || "") || (state.lastAt === cur.lastAt && (state.seen || 0) > (cur.seen || 0))) out[id] = state;
  }
  return out;
}
