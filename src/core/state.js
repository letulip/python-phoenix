/** Small persisted states kept in the kv store: today's session, the placement run, drafts. */

export const sessionKey = (date) => `session:${date}`;

export async function loadSession(store, date) { return store.kvGet(sessionKey(date), null); }
export async function saveSession(store, session) { return store.kvSet(sessionKey(session.date), session); }

export async function markSessionStep(store, date, index, patch) {
  const session = await loadSession(store, date);
  if (!session || !session.steps[index]) return null;
  session.steps[index] = { ...session.steps[index], ...patch };
  await saveSession(store, session);
  return session;
}

export const DIAGNOSTIC_KEY = "diagnostic";
export async function loadDiagnostic(store) { return store.kvGet(DIAGNOSTIC_KEY, null); }
export async function saveDiagnostic(store, state) { return store.kvSet(DIAGNOSTIC_KEY, state); }
export async function clearDiagnostic(store) { return store.kvDelete(DIAGNOSTIC_KEY); }

export async function recordDiagnosticResult(store, result) {
  const state = await loadDiagnostic(store);
  if (!state) return null;
  state.results = (state.results || []).filter((r) => r.taskId !== result.taskId);
  state.results.push(result);
  state.index = Math.min(state.queue.length, (state.index || 0) + 1);
  await saveDiagnostic(store, state);
  return state;
}

export const draftKey = (taskId) => `draft:${taskId}`;

export const CARDS_SEEN_KEY = "cardsSeen";
export async function loadCardsSeen(store) { return store.kvGet(CARDS_SEEN_KEY, []); }
export async function markCardSeen(store, moduleId) {
  const seen = await loadCardsSeen(store);
  if (!seen.includes(moduleId)) { seen.push(moduleId); await store.kvSet(CARDS_SEEN_KEY, seen); }
  return seen;
}

// ---------------------------------------------------------------- idiom gym
import { nextState } from "./srs.js";

export const SRS_KEY = "srs";
export async function loadSrs(store) { return store.kvGet(SRS_KEY, {}); }
export async function saveSrs(store, srs) { return store.kvSet(SRS_KEY, srs); }
/** Update the card of a drill after an attempt; returns the new state. */
export async function recordGymResult(store, drillId, passed, today, at = null) {
  const srs = await loadSrs(store);
  srs[drillId] = nextState(srs[drillId], passed, today, at);
  await saveSrs(store, srs);
  return srs[drillId];
}

export const ROUND_KEY = "gymRound";
export async function loadRound(store) { return store.kvGet(ROUND_KEY, null); }
export async function saveRound(store, round) { return store.kvSet(ROUND_KEY, round); }
export async function markRoundStep(store, index, patch) {
  const round = await loadRound(store);
  if (!round || !round.steps[index]) return null;
  round.steps[index] = { ...round.steps[index], ...patch };
  await saveRound(store, round);
  return round;
}

export const ROUNDS_KEY = "gymRounds";
export async function archiveRound(store, summary) {
  const list = await store.kvGet(ROUNDS_KEY, []);
  list.push(summary);
  await store.kvSet(ROUNDS_KEY, list.slice(-300));
}
