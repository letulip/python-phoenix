#!/usr/bin/env python3
"""Validate the authored exercises and generate content/tasks.json and docs/CURRICULUM.md.

Usage:
  python3 tools/build_content.py           validate, then (re)write the generated files
  python3 tools/build_content.py --check   validate, then fail if the generated files are stale

Authoring format (one file per exercise under content/src/L<level>/<module>/):
  _module.py   MODULE = dict(id, level, order, title_en, title_ru, concepts, card, diagnostic)
  <slug>.py    META = dict(...), STARTER, SOLUTION, TESTS, optional MODEL (retype),
               EXAMPLES (visible examples), SOLUTION_ALT

The gate runs the reference solution against the tests with the same harness the
browser uses (src/runner/runner.py), checks that the starter does not already pass,
and validates every metadata field.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "src"
CONCEPTS_PATH = ROOT / "content" / "concepts.json"
TASKS_PATH = ROOT / "content" / "tasks.json"
CURRICULUM_PATH = ROOT / "docs" / "CURRICULUM.md"
RUNNER_PATH = ROOT / "src" / "runner" / "runner.py"

TYPES = ("retype", "cloze", "task", "refactor")
DRILL_TYPES = ("retype", "cloze")
WORLDS = ("shorts", "bybit", "tennis", "oth", "everyday", "game", "neutral")
ID_RE = re.compile(r"^l(\d)\.([a-z0-9-]+)\.([a-z0-9-]+)$")
MODULE_ID_RE = re.compile(r"^l(\d)\.([a-z0-9-]+)$")
BLANK = "___"
TEST_DEF_RE = re.compile(r"^def test_\w+\(", re.M)

CARD_SNIPPET_KEYS = ("title_en", "title_ru", "code", "note_en", "note_ru")


def load_py(path: Path):
    name = "content_" + re.sub(r"\W", "_", str(path.relative_to(ROOT)))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_runner():
    return load_py(RUNNER_PATH)


class Problems:
    def __init__(self):
        self.items: list[str] = []

    def add(self, where, message):
        self.items.append(f"{where}: {message}")

    def __bool__(self):
        return bool(self.items)


def failing_summary(result):
    if result.get("error"):
        err = result["error"]
        return f"{err['type']} at line {err.get('line')}: {err['message']}"
    bad = [t for t in result.get("tests", []) if t["status"] != "pass"]
    parts = []
    for t in bad[:3]:
        if t["status"] == "fail":
            parts.append(f"{t['name']} [{t.get('label', '')}] expected {t.get('expected')} got {t.get('actual')}")
        else:
            e = t.get("error", {})
            parts.append(f"{t['name']} raised {e.get('type')}: {e.get('message')} (line {e.get('line')})")
    return "; ".join(parts) or "no tests ran"


def require(meta, key, where, problems, kind=None, non_empty=True):
    if key not in meta:
        problems.add(where, f"META.{key} is missing")
        return None
    value = meta[key]
    if kind is not None and not isinstance(value, kind):
        problems.add(where, f"META.{key} must be {getattr(kind, '__name__', kind)}")
        return None
    if non_empty and value in ("", [], None):
        problems.add(where, f"META.{key} is empty")
        return None
    return value


def validate_card(card, where, problems):
    if not isinstance(card, dict):
        problems.add(where, "MODULE.card must be a dict")
        return
    for key in ("intro_en", "intro_ru", "phrase_en"):
        if not card.get(key):
            problems.add(where, f"card.{key} is missing")
    snippets = card.get("snippets") or []
    if not snippets:
        problems.add(where, "card.snippets is empty")
    for i, sn in enumerate(snippets):
        for key in CARD_SNIPPET_KEYS:
            if not sn.get(key):
                problems.add(where, f"card.snippets[{i}].{key} is missing")
        code = sn.get("code") or ""
        if code and len(code.strip().splitlines()) > 14:
            problems.add(where, f"card.snippets[{i}].code is longer than 14 lines")
    for key in ("gotchas_en", "gotchas_ru"):
        if not card.get(key):
            problems.add(where, f"card.{key} is missing")
    if len(card.get("gotchas_en", [])) != len(card.get("gotchas_ru", [])):
        problems.add(where, "card.gotchas_en and gotchas_ru differ in length")


def build(problems: Problems):
    runner = load_runner()
    concepts = json.loads(CONCEPTS_PATH.read_text(encoding="utf-8"))
    modules = []
    tasks = {}
    seen_ids = set()

    module_files = sorted(SRC.glob("L*/*/_module.py"))
    if not module_files:
        problems.add(str(SRC), "no modules found")

    for module_file in module_files:
        where = str(module_file.relative_to(ROOT))
        try:
            mod = load_py(module_file)
        except Exception as exc:  # noqa: BLE001
            problems.add(where, f"failed to import: {exc!r}")
            continue
        info = getattr(mod, "MODULE", None)
        if not isinstance(info, dict):
            problems.add(where, "MODULE dict is missing")
            continue
        mid = info.get("id", "")
        m = MODULE_ID_RE.match(mid)
        if not m:
            problems.add(where, f"bad module id {mid!r}")
            continue
        level_dir = module_file.parent.parent.name  # L0
        if level_dir != f"L{m.group(1)}":
            problems.add(where, f"module id level {mid!r} does not match folder {level_dir}")
        if module_file.parent.name != m.group(2):
            problems.add(where, f"module id {mid!r} does not match folder {module_file.parent.name}")
        for key in ("order", "title_en", "title_ru", "concepts", "card",
                    "chapter_en", "chapter_ru", "story_en", "story_ru", "story_done_en", "story_done_ru"):
            if key not in info or info[key] in ("", None):
                problems.add(where, f"MODULE.{key} is missing")
        for key in ("story_en", "story_ru"):
            if len(str(info.get(key, "")).split()) > 90:
                problems.add(where, f"MODULE.{key} is longer than 90 words – keep the story short")
        for c in info.get("concepts", []):
            if c not in concepts:
                problems.add(where, f"unknown concept {c!r} (add it to content/concepts.json)")
        validate_card(info.get("card", {}), where, problems)

        exercises = []
        for ex_file in sorted(module_file.parent.glob("*.py")):
            if ex_file.name.startswith("_"):
                continue
            ex_where = str(ex_file.relative_to(ROOT))
            entry = build_exercise(ex_file, ex_where, mid, int(m.group(1)), info, concepts, runner, problems)
            if entry is None:
                continue
            if entry["id"] in seen_ids:
                problems.add(ex_where, f"duplicate id {entry['id']}")
            seen_ids.add(entry["id"])
            exercises.append(entry)

        exercises.sort(key=lambda e: (e["order"], e["id"]))
        if not exercises:
            problems.add(where, "module has no exercises")
        ex_ids = [e["id"] for e in exercises]
        diagnostic = list(info.get("diagnostic", []))
        for d in diagnostic:
            if d not in ex_ids:
                problems.add(where, f"diagnostic id {d!r} is not an exercise of this module")
        for e in exercises:
            e["diagnostic"] = e["id"] in diagnostic
            tasks[e["id"]] = e
        modules.append({
            "id": mid, "level": int(m.group(1)), "order": info.get("order", 0),
            "title_en": info.get("title_en", ""), "title_ru": info.get("title_ru", ""),
            "chapter_en": info.get("chapter_en", ""), "chapter_ru": info.get("chapter_ru", ""),
            "story_en": info.get("story_en", ""), "story_ru": info.get("story_ru", ""),
            "story_done_en": info.get("story_done_en", ""), "story_done_ru": info.get("story_done_ru", ""),
            "concepts": list(info.get("concepts", [])), "card": info.get("card", {}),
            "exercises": ex_ids, "diagnostic": diagnostic,
        })

    modules.sort(key=lambda mm: (mm["level"], mm["order"], mm["id"]))
    return {"schema": 1, "concepts": concepts, "modules": modules, "tasks": tasks}


def build_exercise(path, where, module_id, level, module_info, concepts, runner, problems):
    try:
        mod = load_py(path)
    except Exception as exc:  # noqa: BLE001
        problems.add(where, f"failed to import: {exc!r}")
        return None
    meta = getattr(mod, "META", None)
    if not isinstance(meta, dict):
        problems.add(where, "META dict is missing")
        return None

    ex_id = require(meta, "id", where, problems, str) or ""
    m = ID_RE.match(ex_id)
    if not m:
        problems.add(where, f"bad id {ex_id!r}, expected l<level>.<module>.<slug>")
    elif f"l{m.group(1)}.{m.group(2)}" != module_id:
        problems.add(where, f"id {ex_id!r} does not belong to module {module_id}")
    elif m.group(3) != path.stem.replace("_", "-"):
        problems.add(where, f"slug {m.group(3)!r} should match file name {path.stem!r} (underscores become dashes)")

    ex_type = require(meta, "type", where, problems, str)
    if ex_type not in TYPES:
        problems.add(where, f"type must be one of {TYPES}")
    is_drill = ex_type in DRILL_TYPES

    difficulty = require(meta, "difficulty", where, problems, int)
    if difficulty is not None and not 1 <= difficulty <= 5:
        problems.add(where, "difficulty must be 1..5")
    minutes = require(meta, "minutes", where, problems, int)
    if minutes is not None and not 1 <= minutes <= 30:
        problems.add(where, "minutes must be 1..30")
    world = require(meta, "world", where, problems, str)
    if world not in WORLDS:
        problems.add(where, f"world must be one of {WORLDS}")
    ex_concepts = require(meta, "concepts", where, problems, list) or []
    for c in ex_concepts:
        if c not in concepts:
            problems.add(where, f"unknown concept {c!r}")
    if ex_concepts and not any(c in module_info.get("concepts", []) for c in ex_concepts):
        problems.add(where, "none of the concepts belong to the module")

    require(meta, "title", where, problems, str)
    require(meta, "statement_en", where, problems, str)
    hints_en = require(meta, "hints_en", where, problems, list) or []
    hints_ru = require(meta, "hints_ru", where, problems, list) or []
    if len(hints_en) != len(hints_ru):
        problems.add(where, "hints_en and hints_ru differ in length")
    min_hints = 1 if is_drill else 2
    if len(hints_en) < min_hints:
        problems.add(where, f"need at least {min_hints} hints")
    if any(not str(h).strip() for h in hints_en + hints_ru):
        problems.add(where, "empty hint")
    require(meta, "explanation_en", where, problems, str)
    require(meta, "explanation_ru", where, problems, str)
    talk = meta.get("talk_track", [])
    if not is_drill and len(talk) < 2:
        problems.add(where, "talk_track needs at least 2 lines for task/refactor")
    order = meta.get("order", 100)
    if not isinstance(order, int):
        problems.add(where, "order must be an int")
    story = meta.get("story_en", "")
    if story and len(str(story).split()) > 60:
        problems.add(where, "story_en is longer than 60 words – the flavour line must stay short")
    timeout_ms = meta.get("timeout_ms", None)
    if timeout_ms is not None and not 1000 <= timeout_ms <= 20000:
        problems.add(where, "timeout_ms must be 1000..20000")
    for key in ("variants", "followups"):
        if key in meta and not isinstance(meta[key], list):
            problems.add(where, f"META.{key} must be a list")

    starter = getattr(mod, "STARTER", "")
    solution = getattr(mod, "SOLUTION", None)
    solution_alt = getattr(mod, "SOLUTION_ALT", None)
    tests = getattr(mod, "TESTS", None)
    model = getattr(mod, "MODEL", None)
    examples = list(getattr(mod, "EXAMPLES", []) or [])

    if not isinstance(tests, str) or not TEST_DEF_RE.search(tests or ""):
        problems.add(where, "TESTS must define at least one test_ function")
        tests = tests or ""
    if ex_type == "retype":
        if not isinstance(model, str) or not model.strip():
            problems.add(where, "retype needs MODEL (the snippet to retype)")
        solution = solution if isinstance(solution, str) else model
    else:
        if not isinstance(solution, str) or not solution.strip():
            problems.add(where, "SOLUTION is missing")
    if ex_type == "cloze" and BLANK not in starter:
        problems.add(where, f"cloze STARTER must contain blanks {BLANK!r}")
    if ex_type in ("task", "refactor") and not starter.strip():
        problems.add(where, "STARTER must not be empty for task/refactor")
    if isinstance(solution, str) and BLANK in solution:
        problems.add(where, "SOLUTION still contains blanks")

    for i, ex in enumerate(examples):
        if "call" not in ex or not ("expected" in ex or "prints" in ex):
            problems.add(where, f"EXAMPLES[{i}] needs 'call' and 'expected' or 'prints'")

    # Behavioural gate: reference passes, starter does not, examples hold.
    if isinstance(solution, str) and solution.strip() and tests:
        res = runner.run_tests(solution, tests)
        if not res["ok"]:
            problems.add(where, f"SOLUTION fails its own tests: {failing_summary(res)}")
        if examples:
            ex_res = runner.run_code(solution, examples)
            if not ex_res["ok"]:
                bad = [e for e in ex_res["examples"] if e["status"] != "pass"]
                problems.add(where, f"EXAMPLES do not hold for SOLUTION: {bad[:2]}")
        if isinstance(solution_alt, str) and solution_alt.strip():
            res_alt = runner.run_tests(solution_alt, tests)
            if not res_alt["ok"]:
                problems.add(where, f"SOLUTION_ALT fails the tests: {failing_summary(res_alt)}")
        starter_res = runner.run_tests(starter, tests)
        if starter_res["ok"]:
            problems.add(where, "STARTER already passes the tests – the exercise asks nothing")

    return {
        "id": ex_id, "type": ex_type, "level": level, "module": module_id,
        "order": order, "difficulty": difficulty, "minutes": minutes,
        "concepts": ex_concepts, "world": world, "title": meta.get("title", ""),
        "statement_en": meta.get("statement_en", ""),
        "story_en": meta.get("story_en", ""),
        "starter": starter.strip("\n") + ("\n" if starter.strip() else ""),
        "model": (model.strip("\n") + "\n") if isinstance(model, str) and model.strip() else None,
        "examples": examples, "tests": tests,
        "solution": solution.strip("\n") + "\n" if isinstance(solution, str) else "",
        "solution_alt": (solution_alt.strip("\n") + "\n") if isinstance(solution_alt, str) and solution_alt.strip() else None,
        "hints_en": hints_en, "hints_ru": hints_ru,
        "explanation_en": meta.get("explanation_en", ""), "explanation_ru": meta.get("explanation_ru", ""),
        "talk_track": list(talk), "complexity": meta.get("complexity"),
        "variants": list(meta.get("variants", [])), "followups": list(meta.get("followups", [])),
        "timeout_ms": timeout_ms,
    }


def render_curriculum(data):
    lines = ["# Curriculum", "", "Generated by tools/build_content.py – do not edit by hand.", ""]
    total_drills = total_tasks = 0
    for mod in data["modules"]:
        exs = [data["tasks"][i] for i in mod["exercises"]]
        drills = sum(e["type"] in DRILL_TYPES for e in exs)
        tasks = len(exs) - drills
        total_drills += drills
        total_tasks += tasks
        minutes = sum(e["minutes"] for e in exs)
        lines.append(f"## L{mod['level']} · {mod['title_en']} / {mod['title_ru']} (`{mod['id']}`)")
        lines.append("")
        lines.append(f"{mod['chapter_en']} – {mod['story_en']}")
        lines.append("")
        lines.append(f"{len(exs)} exercises: {drills} drills, {tasks} tasks, about {minutes} min. "
                     f"Concepts: {', '.join(mod['concepts'])}.")
        lines.append("")
        lines.append("| # | id | type | diff | min | world | title |")
        lines.append("|---|---|---|---|---|---|---|")
        for i, e in enumerate(exs, 1):
            flag = " ◆" if e["diagnostic"] else ""
            lines.append(f"| {i} | `{e['id']}` | {e['type']} | {e['difficulty']} | {e['minutes']} | {e['world']} | {e['title']}{flag} |")
        lines.append("")
    lines.insert(3, f"Total: {total_drills + total_tasks} exercises ({total_drills} drills, {total_tasks} tasks). ◆ = used in the placement test.")
    lines.insert(4, "")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()

    problems = Problems()
    data = build(problems)
    if problems:
        print("content gate: FAILED", file=sys.stderr)
        for item in problems.items:
            print("  " + item, file=sys.stderr)
        return 1

    tasks_json = json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    curriculum = render_curriculum(data)
    n_drills = sum(t["type"] in DRILL_TYPES for t in data["tasks"].values())
    n_tasks = len(data["tasks"]) - n_drills
    summary = f"{len(data['modules'])} modules, {len(data['tasks'])} exercises ({n_drills} drills, {n_tasks} tasks)"

    if args.check:
        stale = []
        if not TASKS_PATH.exists() or TASKS_PATH.read_text(encoding="utf-8") != tasks_json:
            stale.append(str(TASKS_PATH.relative_to(ROOT)))
        if not CURRICULUM_PATH.exists() or CURRICULUM_PATH.read_text(encoding="utf-8") != curriculum:
            stale.append(str(CURRICULUM_PATH.relative_to(ROOT)))
        if stale:
            print(f"content gate: generated files are stale: {', '.join(stale)} – run `npm run content`", file=sys.stderr)
            return 1
        print(f"content gate: OK – {summary}")
        return 0

    TASKS_PATH.write_text(tasks_json, encoding="utf-8")
    CURRICULUM_PATH.write_text(curriculum, encoding="utf-8")
    print(f"content built: {summary} -> {TASKS_PATH.relative_to(ROOT)}, {CURRICULUM_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
