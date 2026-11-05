/**
 * Pure progress logic (no DOM, no storage): module statuses, the linear session of the day,
 * streaks, placement evaluation and statistics for the progress screen. Tested with node --test.
 */

export const DRILL_TYPES = new Set(["retype", "cloze"]);

export function todayKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function seededRandom(seed) {
  let h = 1779033703 ^ seed.length;
  for (let i = 0; i < seed.length; i++) {
    h = Math.imul(h ^ seed.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  let a = h >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function sortedModules(content) {
  return [...content.modules].sort((a, b) => a.level - b.level || a.order - b.order || a.id.localeCompare(b.id));
}

/** taskId -> { passed: bool, attempts: n, last: attempt } */
export function indexAttempts(attempts) {
  const byTask = new Map();
  for (const a of attempts) {
    const entry = byTask.get(a.taskId) || { passed: false, attempts: 0, last: null, lastPassedAt: null };
    entry.attempts += 1;
    if (a.result === "passed") {
      entry.passed = true;
      if (!entry.lastPassedAt || a.endedAt > entry.lastPassedAt) entry.lastPassedAt = a.endedAt;
    }
    if (!entry.last || (a.startedAt || "") > (entry.last.startedAt || "")) entry.last = a;
    byTask.set(a.taskId, entry);
  }
  return byTask;
}

export function computeModuleStatuses(content, attempts, profile) {
  const byTask = indexAttempts(attempts);
  const known = new Set(profile?.placement?.known || []);
  const result = {};
  let firstOpen = null;
  for (const mod of sortedModules(content)) {
    const total = mod.exercises.length;
    const passed = mod.exercises.filter((id) => byTask.get(id)?.passed).length;
    const tried = mod.exercises.filter((id) => byTask.has(id)).length;
    let status;
    if (total > 0 && passed === total) status = "done";
    else if (known.has(mod.id) && tried === 0) status = "known";
    else if (passed > 0 || tried > 0) status = "active";
    else status = "new";
    if (!firstOpen && (status === "active" || status === "new")) firstOpen = mod.id;
    result[mod.id] = { status, passed, total, tried };
  }
  return { modules: result, currentModule: firstOpen };
}

function pickSome(list, n, random) {
  const pool = [...list];
  const out = [];
  while (pool.length && out.length < n) out.push(pool.splice(Math.floor(random() * pool.length), 1)[0]);
  return out;
}

/**
 * Linear session of the day (wave 1): warm-up drills from earlier modules, the current module's
 * card plus its unpassed exercises within the time budget, and one review task from earlier modules.
 */
export function buildSession({ content, attempts, profile, settings, date, random = Math.random, cardsSeen = [] }) {
  const { modules: statuses, currentModule } = computeModuleStatuses(content, attempts, profile);
  const byTask = indexAttempts(attempts);
  const mods = sortedModules(content);
  const budget = Number(settings?.sessionMinutes) || 30;
  const steps = [];

  const earlier = currentModule ? mods.slice(0, mods.findIndex((m) => m.id === currentModule)) : mods;
  const passedEarlier = earlier.flatMap((m) => m.exercises).filter((id) => byTask.get(id)?.passed);
  const leastRecentFirst = (ids) => [...ids].sort((a, b) =>
    (byTask.get(a)?.lastPassedAt || "").localeCompare(byTask.get(b)?.lastPassedAt || ""));

  // warm-up: up to 3 passed drills, least recently passed first (random among the oldest half)
  const drills = leastRecentFirst(passedEarlier.filter((id) => DRILL_TYPES.has(content.tasks[id]?.type)));
  const warmup = pickSome(drills.slice(0, Math.max(3, Math.ceil(drills.length / 2))), 3, random);
  for (const id of warmup) steps.push({ kind: "exercise", id, role: "warmup", status: "pending", attemptId: null });

  // review candidate: one passed task/refactor from earlier modules
  const reviewPool = leastRecentFirst(passedEarlier.filter((id) => !DRILL_TYPES.has(content.tasks[id]?.type)));
  const review = reviewPool.length ? pickSome(reviewPool.slice(0, Math.max(2, Math.ceil(reviewPool.length / 2))), 1, random)[0] : null;

  if (currentModule) {
    const mod = mods.find((m) => m.id === currentModule);
    const showCard = !cardsSeen.includes(mod.id);
    if (showCard) steps.push({ kind: "card", id: mod.id, role: "card", status: "pending", attemptId: null });
    const warmMinutes = warmup.reduce((s, id) => s + (content.tasks[id]?.minutes || 2), 0);
    const reviewMinutes = review ? (content.tasks[review]?.minutes || 5) : 0;
    let left = budget - warmMinutes - reviewMinutes - (showCard ? 3 : 0);
    const remaining = mod.exercises.filter((id) => !byTask.get(id)?.passed);
    let added = 0;
    for (const id of remaining) {
      const minutes = content.tasks[id]?.minutes || 5;
      if (added >= 2 && left - minutes < 0) break;
      steps.push({ kind: "exercise", id, role: "lesson", status: "pending", attemptId: null });
      left -= minutes;
      added += 1;
    }
  }
  if (review) steps.push({ kind: "exercise", id: review, role: "review", status: "pending", attemptId: null });

  return { date, moduleId: currentModule, steps, startedAt: null, finishedAt: null, recorded: false };
}

export function sessionMinutes(content, session) {
  return session.steps.reduce((sum, s) => sum + (s.kind === "card" ? 3 : (content.tasks[s.id]?.minutes || 0)), 0);
}

/** Consecutive days with a session, ending today or yesterday. sessions: [{date}] */
export function computeStreak(sessions, today = todayKey()) {
  const days = new Set(sessions.map((s) => s.date));
  let cursor = new Date(`${today}T12:00:00`);
  if (!days.has(todayKey(cursor))) cursor.setDate(cursor.getDate() - 1);
  let streak = 0;
  while (days.has(todayKey(cursor))) { streak += 1; cursor.setDate(cursor.getDate() - 1); }
  return streak;
}

/** results: [{taskId, passed, activeSec, runs, hintsUsed}] -> placement */
export function evaluatePlacement(content, results, at = new Date().toISOString()) {
  const byTask = new Map(results.map((r) => [r.taskId, r]));
  const known = [];
  for (const mod of sortedModules(content)) {
    if (!mod.diagnostic.length) continue;
    const ok = mod.diagnostic.every((id) => {
      const r = byTask.get(id);
      const limit = (content.tasks[id]?.minutes || 5) * 60 * 1.5;
      return r && r.passed && (r.runs || 0) <= 3 && (r.hintsUsed || 0) === 0 && (r.activeSec || 0) <= limit;
    });
    if (ok) known.push(mod.id);
  }
  const startModule = sortedModules(content).find((m) => !known.includes(m.id))?.id || null;
  return { at, known, startModule, results };
}

function median(values) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : Math.round((sorted[mid - 1] + sorted[mid]) / 2);
}

export function aggregateStats(content, attempts) {
  const byTask = indexAttempts(attempts);
  const finished = attempts.filter((a) => a.result && a.result !== "left");
  const passed = finished.filter((a) => a.result === "passed");
  const totalExercises = Object.keys(content.tasks).length;
  const passedExercises = Object.keys(content.tasks).filter((id) => byTask.get(id)?.passed).length;

  const byModule = {};
  for (const mod of sortedModules(content)) {
    byModule[mod.id] = { passed: mod.exercises.filter((id) => byTask.get(id)?.passed).length, total: mod.exercises.length };
  }

  const conceptAcc = {};
  for (const a of finished) {
    const task = content.tasks[a.taskId];
    if (!task) continue;
    for (const c of task.concepts) {
      const acc = conceptAcc[c] || (conceptAcc[c] = { id: c, attempts: 0, passed: 0, hints: 0, secs: [] });
      acc.attempts += 1;
      if (a.result === "passed") { acc.passed += 1; acc.secs.push(a.activeSec || 0); }
      acc.hints += a.hintsUsed || 0;
    }
  }
  const byConcept = Object.values(conceptAcc).map((c) => ({
    id: c.id, attempts: c.attempts, passed: c.passed,
    passRate: c.attempts ? c.passed / c.attempts : 0,
    hintsAvg: c.attempts ? c.hints / c.attempts : 0,
    medianSec: median(c.secs),
  })).sort((a, b) => a.passRate - b.passRate || b.attempts - a.attempts || a.id.localeCompare(b.id));

  const errorAcc = {};
  for (const a of finished) for (const e of a.errors || []) errorAcc[e.type] = (errorAcc[e.type] || 0) + e.count;
  const errors = Object.entries(errorAcc).map(([type, count]) => ({ type, count })).sort((a, b) => b.count - a.count);

  const byType = {};
  for (const a of finished) {
    const acc = byType[a.type] || (byType[a.type] = { attempts: 0, passed: 0, secs: [] });
    acc.attempts += 1;
    if (a.result === "passed") { acc.passed += 1; acc.secs.push(a.activeSec || 0); }
  }
  for (const t of Object.values(byType)) { t.medianSec = median(t.secs); delete t.secs; }

  const noHint = passed.length ? passed.filter((a) => !a.hintsUsed).length / passed.length : 0;
  return { totalExercises, passedExercises, attempts: finished.length, passedAttempts: passed.length, byModule, byConcept, errors, byType, noHintRate: noHint };
}

/** Per-concept mastery summary for the export (wave 1: derived counts; SRS fields arrive in wave 2). */
export function masterySnapshot(content, attempts) {
  const out = {};
  for (const c of aggregateStats(content, attempts).byConcept) {
    out[c.id] = { attempts: c.attempts, passed: c.passed, passRate: Number(c.passRate.toFixed(2)), hintsAvg: Number(c.hintsAvg.toFixed(2)), medianSec: c.medianSec };
  }
  return out;
}
