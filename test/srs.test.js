import { test } from "node:test";
import assert from "node:assert/strict";
import { INTERVALS, MAX_BOX, addDays, nextState, pickVariant, buildRound, familySummary, gymCounts, mergeSrs } from "../src/core/srs.js";

function drill(id, order, variants = 1) {
  return { id, type: "rewrite", minutes: 1, order, variants: Array.from({ length: variants }, () => ({})) };
}
const content = {
  gym: { families: [
    { id: "gym.a", tier: 1, order: 1, drills: ["gym.a.1", "gym.a.2", "gym.a.3"] },
    { id: "gym.b", tier: 1, order: 2, drills: ["gym.b.1", "gym.b.2", "gym.b.3"] },
    { id: "gym.c", tier: 2, order: 1, drills: ["gym.c.1"] },
  ] },
  tasks: {
    "gym.a.1": drill("gym.a.1", 10, 3), "gym.a.2": drill("gym.a.2", 20), "gym.a.3": drill("gym.a.3", 30),
    "gym.b.1": drill("gym.b.1", 10), "gym.b.2": drill("gym.b.2", 20), "gym.b.3": drill("gym.b.3", 30),
    "gym.c.1": drill("gym.c.1", 10),
  },
};
const TODAY = "2026-11-07";

test("addDays crosses month and year boundaries", () => {
  assert.equal(addDays("2026-11-30", 1), "2026-12-01");
  assert.equal(addDays("2026-12-31", 1), "2027-01-01");
  assert.equal(addDays(TODAY, 0), TODAY);
});

test("a pass climbs one box, a fail drops to zero and returns tomorrow", () => {
  const first = nextState(null, true, TODAY, "2026-11-07T10:00:00Z");
  assert.equal(first.box, 1);
  assert.equal(first.due, addDays(TODAY, INTERVALS[1]));
  assert.deepEqual([first.seen, first.passes, first.fails, first.lastResult], [1, 1, 0, "passed"]);
  const failed = nextState(first, false, TODAY);
  assert.equal(failed.box, 0);
  assert.equal(failed.due, addDays(TODAY, 1));
  assert.deepEqual([failed.seen, failed.passes, failed.fails], [2, 1, 1]);
  let s = first;
  for (let i = 0; i < 10; i++) s = nextState(s, true, TODAY);
  assert.equal(s.box, MAX_BOX);
  assert.equal(s.due, addDays(TODAY, INTERVALS[MAX_BOX]));
});

test("variants rotate with the attempts made so far", () => {
  assert.equal(pickVariant(null, 3), 0);
  assert.equal(pickVariant({ seen: 1 }, 3), 1);
  assert.equal(pickVariant({ seen: 3 }, 3), 0);
  assert.equal(pickVariant({ seen: 5 }, 1), 0);
});

test("first round interleaves new drills across tier-1 families", () => {
  const round = buildRound({ content, srs: {}, today: TODAY });
  assert.deepEqual(round.steps.map((s) => s.id), ["gym.a.1", "gym.b.1", "gym.a.2", "gym.b.2", "gym.a.3"]);
  assert.ok(round.steps.every((s) => s.status === "pending" && s.variant === 0));
});

test("overdue cards come first, most overdue first, then new ones; neighbours differ in family", () => {
  const srs = {
    "gym.b.3": { box: 1, due: "2026-11-05", seen: 1 },
    "gym.a.3": { box: 2, due: "2026-11-06", seen: 2 },
    "gym.a.1": { box: 3, due: "2026-11-20", seen: 4 },
  };
  const round = buildRound({ content, srs, today: TODAY });
  assert.deepEqual(round.steps.slice(0, 2).map((s) => s.id), ["gym.b.3", "gym.a.3"]);
  assert.equal(round.steps.length, 5);
  for (let i = 1; i < round.steps.length; i++) assert.notEqual(round.steps[i].family, round.steps[i - 1].family, `step ${i}`);
  assert.ok(!round.steps.some((s) => s.id === "gym.a.1"), "a card due in two weeks is not picked while new ones exist");
});

test("a card seen four times gets variant 4 mod 3 = 1", () => {
  const srs = { "gym.a.1": { box: 0, due: "2026-11-06", seen: 4 } };
  const round = buildRound({ content, srs, today: TODAY });
  assert.equal(round.steps[0].id, "gym.a.1");
  assert.equal(round.steps[0].variant, 1);
});

test("a family round stays inside the family and fills from not-due cards when needed", () => {
  const srs = { "gym.b.1": { box: 4, due: "2026-12-01", seen: 5 } };
  const round = buildRound({ content, srs, today: TODAY, familyId: "gym.b" });
  assert.deepEqual(round.steps.map((s) => s.id), ["gym.b.2", "gym.b.3", "gym.b.1"]);
  assert.equal(round.familyId, "gym.b");
});

test("family summary and gym counts", () => {
  const srs = {
    "gym.a.1": { box: 3, due: "2026-11-14", seen: 3, passes: 3, fails: 0 },
    "gym.a.2": { box: 0, due: "2026-11-06", seen: 2, passes: 1, fails: 1 },
  };
  const [a, b, c] = familySummary(content, srs, TODAY);
  assert.deepEqual([a.id, a.total, a.seen, a.fresh, a.due, a.mastered], ["gym.a", 3, 2, 1, 1, 1]);
  assert.equal(a.mastery, 3 / (3 * MAX_BOX));
  assert.equal(a.nextDue, "2026-11-06");
  assert.deepEqual([a.passes, a.fails], [4, 1]);
  assert.deepEqual([b.seen, b.fresh, c.tier], [0, 3, 2]);
  assert.deepEqual(gymCounts(content, srs, TODAY), { total: 7, seen: 2, fresh: 5, due: 1, mastered: 1 });
});

test("merging srs maps keeps the later attempt per drill", () => {
  const local = { x: { box: 1, lastAt: "2026-11-05T10:00:00Z", seen: 1 }, y: { box: 2, lastAt: "2026-11-07T10:00:00Z", seen: 2 } };
  const imported = { x: { box: 2, lastAt: "2026-11-06T10:00:00Z", seen: 2 }, y: { box: 0, lastAt: "2026-11-06T10:00:00Z", seen: 1 }, z: { box: 1, lastAt: "2026-11-01T00:00:00Z", seen: 1 } };
  const merged = mergeSrs(local, imported);
  assert.deepEqual([merged.x.box, merged.y.box, merged.z.box], [2, 2, 1]);
  assert.deepEqual(mergeSrs(local, local), local);
});
