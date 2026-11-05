/** Line-level diff used by retype drills to show where the typed code strays from the model. */

function normalize(text) {
  return text.replace(/\r\n?/g, "\n").split("\n").map((l) => l.replace(/\s+$/, ""));
}

function trimBlankEdges(lines) {
  let start = 0;
  let end = lines.length;
  while (start < end && lines[start] === "") start++;
  while (end > start && lines[end - 1] === "") end--;
  return lines.slice(start, end);
}

/** Returns [{type: "same"|"add"|"del", text}] where "del" lines are in the model but missing
 *  from the typed text, and "add" lines were typed but are not in the model. */
export function lineDiff(modelText, typedText) {
  const a = trimBlankEdges(normalize(modelText));
  const b = trimBlankEdges(normalize(typedText));
  const n = a.length;
  const m = b.length;
  const lcs = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      lcs[i][j] = a[i] === b[j] ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
    }
  }
  const out = [];
  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) { out.push({ type: "same", text: a[i] }); i++; j++; }
    else if (lcs[i + 1][j] >= lcs[i][j + 1]) { out.push({ type: "del", text: a[i] }); i++; }
    else { out.push({ type: "add", text: b[j] }); j++; }
  }
  while (i < n) out.push({ type: "del", text: a[i++] });
  while (j < m) out.push({ type: "add", text: b[j++] });
  return out;
}

/** True when the typed text matches the model line by line (ignoring trailing spaces and blank edges). */
export function sameLines(modelText, typedText) {
  return lineDiff(modelText, typedText).every((d) => d.type === "same");
}
