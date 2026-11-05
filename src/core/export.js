/** Progress export/import: schema 1 (see docs/SPEC.md §8). Pure functions, tested in node. */
import { computeModuleStatuses, masterySnapshot } from "./progress.js";

export const SCHEMA = 1;
export const APP_ID = "python-phoenix";

export function buildExport({ version, profile, settings, attempts, events, sessions, content, now = new Date() }) {
  const statuses = content ? computeModuleStatuses(content, attempts, profile).modules : {};
  const modules = Object.fromEntries(Object.entries(statuses).map(([id, s]) => [id, { status: s.status, passed: s.passed, total: s.total }]));
  return {
    schema: SCHEMA, app: APP_ID, appVersion: version, exportedAt: now.toISOString(),
    profile: { startedAt: profile?.startedAt || null, placement: profile?.placement || null, settings: settings || {} },
    attempts: [...attempts].sort((a, b) => String(a.startedAt).localeCompare(String(b.startedAt))),
    mastery: content ? masterySnapshot(content, attempts) : {},
    modules,
    sessions: [...sessions].sort((a, b) => a.date.localeCompare(b.date)),
    events: [...events].sort((a, b) => String(a.t).localeCompare(String(b.t))).slice(-5000),
  };
}

export function validateImport(obj) {
  if (!obj || typeof obj !== "object") throw new Error("not an object");
  if (obj.app !== APP_ID) throw new Error(`app is ${JSON.stringify(obj.app)}`);
  if (obj.schema !== SCHEMA) throw new Error(`schema ${obj.schema} is not supported`);
  if (!Array.isArray(obj.attempts)) throw new Error("attempts is not a list");
  for (const a of obj.attempts) {
    if (!a.id || !a.taskId) throw new Error("an attempt lacks id or taskId");
  }
  return true;
}

/** Merge an imported export into the local state. Records merge by id; local profile/settings win
 *  unless the local install is fresh (no attempts). Idempotent: importing the same file twice changes nothing. */
export function mergeImport(local, imported) {
  validateImport(imported);
  const fresh = (local.attempts || []).length === 0;
  const attempts = new Map((local.attempts || []).map((a) => [a.id, a]));
  for (const a of imported.attempts) if (!attempts.has(a.id)) attempts.set(a.id, a);
  const events = new Map((local.events || []).map((e) => [e.id, e]));
  for (const e of imported.events || []) if (e && e.id && !events.has(e.id)) events.set(e.id, e);
  const sessions = new Map((local.sessions || []).map((s) => [s.date, s]));
  for (const s of imported.sessions || []) {
    const cur = sessions.get(s.date);
    if (!cur) sessions.set(s.date, s);
    else sessions.set(s.date, { ...cur, minutes: Math.max(cur.minutes || 0, s.minutes || 0), items: Math.max(cur.items || 0, s.items || 0) });
  }
  const importedProfile = imported.profile || {};
  const profile = fresh
    ? { startedAt: importedProfile.startedAt || local.profile?.startedAt || null, placement: importedProfile.placement || null }
    : { ...local.profile, placement: local.profile?.placement || importedProfile.placement || null,
        startedAt: [local.profile?.startedAt, importedProfile.startedAt].filter(Boolean).sort()[0] || null };
  const settings = fresh && importedProfile.settings ? { ...local.settings, ...importedProfile.settings } : local.settings;
  return {
    profile, settings,
    attempts: [...attempts.values()].sort((a, b) => String(a.startedAt).localeCompare(String(b.startedAt))),
    events: [...events.values()].sort((a, b) => String(a.t).localeCompare(String(b.t))),
    sessions: [...sessions.values()].sort((a, b) => a.date.localeCompare(b.date)),
    added: { attempts: attempts.size - (local.attempts || []).length },
  };
}
