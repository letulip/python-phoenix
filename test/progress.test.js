import { test } from "node:test";
import assert from "node:assert/strict";
import { buildSession, computeModuleStatuses, computeStreak, evaluatePlacement, aggregateStats, seededRandom } from "../src/core/progress.js";

function task(id, type, minutes, concepts = ["c1"]) {
  return { id, type, minutes, concepts, difficulty: 1, module: id.split(".").slice(0, 2).join(".") };
}
const content = {
  concepts: { c1: { en: "c1", ru: "c1" }, c2: { en: "c2", ru: "c2" } },
  modules: [
    { id: "l0.a", level: 0, order: 1, exercises: ["l0.a.r1", "l0.a.c1", "l0.a.t1", "l0.a.t2"], diagnostic: ["l0.a.t1"] },
    { id: "l0.b", level: 0, order: 2, exercises: ["l0.b.r1", "l0.b.t1"], diagnostic: ["l0.b.t1"] },
  ],
  tasks: {
    "l0.a.r1": task("l0.a.r1", "retype", 3), "l0.a.c1": task("l0.a.c1", "cloze", 2),
    "l0.a.t1": task("l0.a.t1", "task", 6), "l0.a.t2": task("l0.a.t2", "task", 7, ["c2"]),
    "l0.b.r1": task("l0.b.r1", "retype", 3), "l0.b.t1": task("l0.b.t1", "task", 8),
  },
};
const passed = (taskId, startedAt = "2026-11-05T10:00:00Z", extra = {}) =>
  ({ id: `a-${taskId}-${startedAt}`, taskId, type: content.tasks[taskId].type, result: "passed", startedAt, endedAt: startedAt, activeSec: 100, hintsUsed: 0, errors: [], ...extra });

test("day one: card then the whole module within budget, no warm-up or review", () => {
  const s = buildSession({ content, attempts: [], profile: null, settings: { sessionMinutes: 30 }, date: "2026-11-05", random: seededRandom("x") });
  assert.equal(s.moduleId, "l0.a");
  assert.deepEqual(s.steps.map((x) => `${x.role}:${x.id}`), ["card:l0.a", "lesson:l0.a.r1", "lesson:l0.a.c1", "lesson:l0.a.t1", "lesson:l0.a.t2"]);
});

test("budget caps lesson items but keeps at least two", () => {
  const s = buildSession({ content, attempts: [], profile: null, settings: { sessionMinutes: 5 }, date: "2026-11-05", random: seededRandom("x") });
  assert.deepEqual(s.steps.filter((x) => x.role === "lesson").map((x) => x.id), ["l0.a.r1", "l0.a.c1"]);
});

test("a card already read is not scheduled again", () => {
  const s = buildSession({ content, attempts: [], profile: null, settings: { sessionMinutes: 30 }, date: "2026-11-05", random: seededRandom("x"), cardsSeen: ["l0.a"] });
  assert.equal(s.steps.some((x) => x.kind === "card"), false);
});

test("after module a: warm-up drills and a review come from module a, card for module b", () => {
  const attempts = ["l0.a.r1", "l0.a.c1", "l0.a.t1", "l0.a.t2"].map((id) => passed(id));
  const s = buildSession({ content, attempts, profile: null, settings: { sessionMinutes: 30 }, date: "2026-11-06", random: seededRandom("y"), cardsSeen: ["l0.a"] });
  assert.equal(s.moduleId, "l0.b");
  const roles = s.steps.map((x) => x.role);
  assert.deepEqual(roles.filter((r) => r === "warmup").length, 2); // only two drills exist in module a
  assert.ok(s.steps.some((x) => x.role === "card" && x.id === "l0.b"));
  assert.ok(s.steps.some((x) => x.role === "review" && ["l0.a.t1", "l0.a.t2"].includes(x.id)));
  assert.deepEqual(s.steps.filter((x) => x.role === "lesson").map((x) => x.id), ["l0.b.r1", "l0.b.t1"]);
});

test("module statuses: done, active, new, known", () => {
  const attempts = [passed("l0.a.r1"), { ...passed("l0.a.c1"), result: "failed" }];
  const r = computeModuleStatuses(content, attempts, { placement: { known: ["l0.b"] } });
  assert.equal(r.modules["l0.a"].status, "active");
  assert.equal(r.modules["l0.b"].status, "known");
  assert.equal(r.currentModule, "l0.a");
  const all = ["l0.a.r1", "l0.a.c1", "l0.a.t1", "l0.a.t2"].map((id) => passed(id));
  assert.equal(computeModuleStatuses(content, all, null).modules["l0.a"].status, "done");
  assert.equal(computeModuleStatuses(content, [], null).modules["l0.b"].status, "new");
});

test("streak counts consecutive days ending today or yesterday", () => {
  const sessions = [{ date: "2026-11-03" }, { date: "2026-11-04" }, { date: "2026-11-05" }];
  assert.equal(computeStreak(sessions, "2026-11-05"), 3);
  assert.equal(computeStreak(sessions, "2026-11-06"), 3);
  assert.equal(computeStreak(sessions, "2026-11-07"), 0);
});

test("placement marks a module known only for a clean, quick pass", () => {
  const p = evaluatePlacement(content, [
    { taskId: "l0.a.t1", passed: true, activeSec: 200, runs: 2, hintsUsed: 0 },
    { taskId: "l0.b.t1", passed: true, activeSec: 2000, runs: 2, hintsUsed: 0 },
  ], "2026-11-05T10:00:00Z");
  assert.deepEqual(p.known, ["l0.a"]);
  assert.equal(p.startModule, "l0.b");
});

test("stats aggregate concepts, errors and no-hint rate", () => {
  const attempts = [
    passed("l0.a.t1", "2026-11-05T10:00:00Z", { errors: [{ type: "NameError", count: 2 }] }),
    passed("l0.a.t2", "2026-11-05T11:00:00Z", { hintsUsed: 1 }),
    { ...passed("l0.a.c1", "2026-11-05T12:00:00Z"), result: "gaveUp" },
  ];
  const s = aggregateStats(content, attempts);
  assert.equal(s.passedExercises, 2);
  assert.equal(s.attempts, 3);
  assert.deepEqual(s.errors, [{ type: "NameError", count: 2 }]);
  assert.equal(s.noHintRate, 0.5);
  const c1 = s.byConcept.find((c) => c.id === "c1");
  assert.equal(c1.attempts, 2);
  assert.equal(c1.passed, 1);
});
