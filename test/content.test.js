import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const content = JSON.parse(readFileSync(new URL("../content/tasks.json", import.meta.url), "utf8"));
const REQUIRED = ["id", "type", "level", "module", "difficulty", "minutes", "concepts", "world", "title", "statement_en",
  "starter", "tests", "solution", "hints_en", "hints_ru", "explanation_en", "explanation_ru", "talk_track", "order", "diagnostic"];

test("tasks.json has schema 1 and at least one module", () => {
  assert.equal(content.schema, 1);
  assert.ok(content.modules.length >= 1);
});

test("every exercise is complete and referenced by exactly one module", () => {
  const seen = new Map();
  for (const mod of content.modules) {
    for (const id of mod.exercises) {
      assert.ok(content.tasks[id], `${id} missing from tasks`);
      seen.set(id, (seen.get(id) || 0) + 1);
    }
    for (const c of mod.concepts) assert.ok(content.concepts[c], `unknown concept ${c}`);
    for (const key of ["chapter_en", "chapter_ru", "story_en", "story_ru", "card"]) assert.ok(mod[key], `${mod.id} lacks ${key}`);
  }
  for (const [id, task] of Object.entries(content.tasks)) {
    for (const key of REQUIRED) assert.ok(key in task, `${id} lacks ${key}`);
    assert.match(task.tests, /def test_/);
    assert.equal(seen.get(id), 1, `${id} referenced ${seen.get(id)} times`);
    if (task.type === "retype") assert.ok(task.model, `${id} retype without model`);
    if (task.type === "cloze") assert.match(task.starter, /___/);
    assert.ok(task.hints_en.length === task.hints_ru.length);
  }
});
