import { test } from "node:test";
import assert from "node:assert/strict";
import { buildExport, mergeImport, validateImport } from "../src/core/export.js";

const content = { modules: [{ id: "l0.a", level: 0, order: 1, exercises: ["l0.a.t1"], diagnostic: [] }], tasks: { "l0.a.t1": { id: "l0.a.t1", type: "task", concepts: ["c1"], minutes: 5 } }, concepts: { c1: {} } };
const attempt = (id, taskId = "l0.a.t1") => ({ id, taskId, type: "task", result: "passed", startedAt: `2026-11-05T10:0${id}:00Z`, endedAt: "2026-11-05T10:05:00Z", activeSec: 60, hintsUsed: 0, errors: [] });

test("export has the schema fields and derived module statuses", () => {
  const out = buildExport({ version: "0.1.0", profile: { startedAt: "2026-11-01T00:00:00Z", placement: null }, settings: { lang: "ru" },
    attempts: [attempt("1")], events: [{ id: "e1", t: "2026-11-05T10:00:00Z", k: "run" }], sessions: [{ date: "2026-11-05", minutes: 20 }], content, now: new Date("2026-11-05T12:00:00Z") });
  assert.equal(out.schema, 1);
  assert.equal(out.app, "python-phoenix");
  assert.equal(out.modules["l0.a"].status, "done");
  assert.equal(out.mastery.c1.passed, 1);
  assert.equal(out.exportedAt, "2026-11-05T12:00:00.000Z");
  assert.ok(validateImport(out));
});

test("import merges by id and is idempotent", () => {
  const local = { profile: { startedAt: "2026-11-02T00:00:00Z", placement: { known: ["l0.a"] } }, settings: { lang: "ru" }, attempts: [attempt("1")], events: [], sessions: [{ date: "2026-11-05", minutes: 10, items: 2 }] };
  const file = buildExport({ version: "0.1.0", profile: { startedAt: "2026-11-01T00:00:00Z", placement: null }, settings: { lang: "en" },
    attempts: [attempt("1"), attempt("2")], events: [{ id: "e1", t: "2026-11-05T10:00:00Z", k: "run" }], sessions: [{ date: "2026-11-05", minutes: 25, items: 3 }, { date: "2026-11-04", minutes: 5, items: 1 }], content });
  const once = mergeImport(local, file);
  assert.equal(once.attempts.length, 2);
  assert.equal(once.added.attempts, 1);
  assert.equal(once.settings.lang, "ru", "local settings win on a non-fresh install");
  assert.equal(once.profile.startedAt, "2026-11-01T00:00:00Z", "earliest start date wins");
  assert.deepEqual(once.profile.placement, { known: ["l0.a"] });
  assert.deepEqual(once.sessions.map((s) => `${s.date}:${s.minutes}:${s.items}`), ["2026-11-04:5:1", "2026-11-05:25:3"]);
  const twice = mergeImport({ ...local, attempts: once.attempts, events: once.events, sessions: once.sessions }, file);
  assert.equal(twice.attempts.length, 2);
  assert.equal(twice.added.attempts, 0);
});

test("a fresh install takes the imported profile and settings", () => {
  const file = buildExport({ version: "0.1.0", profile: { startedAt: "2026-11-01T00:00:00Z", placement: { known: [] } }, settings: { lang: "en", sessionMinutes: 45 }, attempts: [attempt("1")], events: [], sessions: [], content });
  const merged = mergeImport({ profile: { startedAt: "2026-11-05T00:00:00Z", placement: null }, settings: { lang: "ru", sessionMinutes: 30 }, attempts: [], events: [], sessions: [] }, file);
  assert.equal(merged.settings.lang, "en");
  assert.equal(merged.settings.sessionMinutes, 45);
  assert.equal(merged.profile.startedAt, "2026-11-01T00:00:00Z");
});

test("validateImport rejects foreign files", () => {
  assert.throws(() => validateImport({ app: "other", schema: 1, attempts: [] }), /app is/);
  assert.throws(() => validateImport({ app: "python-phoenix", schema: 2, attempts: [] }), /schema/);
  assert.throws(() => validateImport({ app: "python-phoenix", schema: 1, attempts: [{ id: "x" }] }), /taskId/);
});
