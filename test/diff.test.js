import { test } from "node:test";
import assert from "node:assert/strict";
import { lineDiff, sameLines, charDiff } from "../src/core/diff.js";

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

test("charDiff isolates a single extra space in a padded line", () => {
  const expected = "'" + "tea".padEnd(10) + " x" + " 2" + "  " + "3.00".padStart(7) + "'";
  const actual = "'" + "tea".padEnd(10) + " x " + " 2" + "  " + "3.00".padStart(7) + "'";
  const d = charDiff(expected, actual);
  assert.equal(d.aMid, "");
  assert.equal(d.bMid, " ");
  assert.equal(d.prefix + d.aMid + d.suffix, expected);
  assert.equal(d.prefix + d.bMid + d.suffix, actual);
});

test("charDiff keeps the common prefix and suffix apart from the change", () => {
  assert.deepEqual(charDiff("abcd", "abXd"), { prefix: "ab", aMid: "c", bMid: "X", suffix: "d" });
  assert.deepEqual(charDiff("same", "same"), { prefix: "same", aMid: "", bMid: "", suffix: "" });
  assert.deepEqual(charDiff("ab", "abab"), { prefix: "ab", aMid: "", bMid: "ab", suffix: "" });
  assert.deepEqual(charDiff("", "x"), { prefix: "", aMid: "", bMid: "x", suffix: "" });
});
