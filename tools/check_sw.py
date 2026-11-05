#!/usr/bin/env python3
"""Gate: every file the app shell needs offline is listed in sw.js SHELL, and nothing listed is missing."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
m = re.search(r"const SHELL = \[(.*?)\];", sw, re.S)
if not m:
    print("check_sw: SHELL list not found in sw.js", file=sys.stderr); sys.exit(1)
listed = set(re.findall(r'"\./([^"]+)"', m.group(1)))
wanted = {"index.html", "styles.css", "app.js", "manifest.json", "content/tasks.json", "vendor/codemirror.js",
          "icons/icon.svg", "icons/icon-192.png", "icons/icon-512.png"}
for p in (ROOT / "src").rglob("*"):
    if p.suffix in (".js", ".py"):
        wanted.add(p.relative_to(ROOT).as_posix())
missing = sorted(wanted - listed)
stale = sorted(f for f in listed if not (ROOT / f).exists())
if missing or stale:
    if missing: print("check_sw: not precached: " + ", ".join(missing), file=sys.stderr)
    if stale: print("check_sw: listed but missing on disk: " + ", ".join(stale), file=sys.stderr)
    sys.exit(1)
print(f"check_sw: OK – {len(listed)} shell files")
