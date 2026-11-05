import { test } from "node:test";
import assert from "node:assert/strict";
import { lineDiff, sameLines } from "../src/core/diff.js";

test("same lines ignore trailing spaces and blank edges", () => {
  assert.equal(sameLines("a\nb\n", "\na\nb  \n\n"), true);
  assert.equal(sameLines("a\nb", "a\nB"), false);
});

test("diff marks missing model lines and extra typed lines", () => {
  const d = lineDiff("a\nb\nc", "a\nc\nd");
  assert.deepEqual(d, [
    { type: "same", text: "a" }, { type: "del", text: "b" }, { type: "same", text: "c" }, { type: "add", text: "d" },
  ]);
});
