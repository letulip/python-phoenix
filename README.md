# Python Phoenix

A browser-only training stand for rebuilding hands-on Python before live-coding interviews. The learner types code by
hand (pasting is blocked in drills), the code runs in a real CPython 3.14 inside the browser (Pyodide in a Web Worker),
hidden tests decide, and every attempt is logged to a JSON export that can be analysed later.

Wave 1 ships the engine and Act I of the storyline: six L0 modules, 45 exercises, about 175 minutes of practice.

## Using it

- Live: `https://letulip.github.io/python-phoenix/` (GitHub Pages, served from `main`).
- Locally: any static server from the repo root, for example `python3 -m http.server 8126`, then open
  `http://127.0.0.1:8126/`. The first load fetches Pyodide (~12 MB) from jsDelivr; afterwards the service worker serves
  everything offline. Append `?nosw` to the URL to bypass the service worker while debugging.
- Desktop first (Chrome or Safari on macOS). Shortcuts in the editor: `Cmd/Ctrl+Enter` runs your code against the
  visible examples, `Shift+Cmd/Ctrl+Enter` runs the hidden tests, `Tab` indents by four spaces.

## What a session looks like

1. Placement test on the first visit: one exercise per module, no hints. Modules you still remember are marked known.
2. Session of the day (25–30 min): warm-up drills from earlier modules, the module card (a short story chapter plus the
   concept card), the module's exercises within the time budget, one review task.
3. Exercise types: `retype` (type the model by hand), `cloze` (fill the `___` blanks), `task` (write the function),
   `refactor` (rewrite without changing behaviour; tests also check the structure through `ast`).
4. Hints open one at a time and are logged; the solution can be revealed; giving up shows the explanation and talk track.
5. Progress → *Download JSON* once a week. Keep the file in `progress/` (or paste it into chat) for the joint analysis.

## Repository layout

```
index.html app.js styles.css sw.js manifest.json   app shell (vanilla ES modules, no build step)
src/ui/            screens: home, session, card, task, map, progress, settings, diagnostic
src/core/          progress.js (session, statuses, stats), export.js (schema 1), store.js (IndexedDB), state.js, diff.js
src/runner/        client.js (worker pool + timeouts), worker.js (Pyodide bootstrap), runner.py (test harness)
src/editor/        CodeMirror 6 wrapper (no autocomplete, paste guard, shortcuts)
vendor/            codemirror.js, built once with esbuild from tools/vendor-entry.js
content/src/       authored exercises, one .py per exercise plus _module.py per module
content/tasks.json generated; content/concepts.json is the concept registry
tools/             build_content.py (validate + generate), check_sw.py, check.sh (the gate)
test/              node --test suites for the pure modules and the runner client
docs/              SPEC.md (the specification, Russian), CURRICULUM.md (generated)
progress/          weekly JSON exports from the owner
```

## Development

```
npm install            # esbuild + CodeMirror, only needed for tests and the vendor bundle
npm run content        # validate every exercise and regenerate content/tasks.json + docs/CURRICULUM.md
npm test               # node --test
npm run check          # the full gate: content --check, service-worker precache list, node tests
npm run build:vendor   # rebuild vendor/codemirror.js after bumping CodeMirror
```

The content gate runs each reference solution against its tests with the same harness the browser uses
(`src/runner/runner.py`), checks that the starter does not already pass, that visible examples hold, that every hint,
explanation and story field exists in both languages where required, and that ids, concepts and worlds are valid.

### Authoring an exercise

```python
META = dict(
    id="l0.functions.cat-years", type="task", order=60,        # l<level>.<module>.<slug>, slug == file name with dashes
    difficulty=1, minutes=5, world="everyday",                  # worlds: shorts bybit tennis oth everyday game neutral
    concepts=["def-return", "early-return"],                   # ids from content/concepts.json
    story_en="One flavour line above the statement.",
    title="Cat years", statement_en="...",                      # statements are English only
    hints_en=[...], hints_ru=[...],                             # same length; 2+ for task/refactor, 1+ for drills
    explanation_en="...", explanation_ru="...",
    talk_track=["what to say to the interviewer", ...],         # required for task/refactor
    complexity="O(1)", followups=[...], variants=[...], timeout_ms=5000,
)
STARTER = "def cat_age(human_years):\n    ...\n"                 # cloze starters contain ___ blanks; retype uses MODEL
EXAMPLES = [{"call": "cat_age(1)", "expected": "15"}]           # or {"call": ..., "prints": "..."}
SOLUTION = "..."; SOLUTION_ALT = "..."                          # the alternative is optional
TESTS = '''
def test_first_year(ns, check):
    check(ns["cat_age"](1), 15, "cat_age(1)")
'''
```

Test functions receive fixtures by parameter name: `ns` (the learner's namespace), `src` (their source), `stdout`,
`check(actual, expected, label)`, `approx`, `capture(fn, *args)`, `raises(ExcType, fn, *args)` and `ast_tools`
(`count_calls`, `count_fstrings`, `has_loop`, `has_comprehension`, `count_nodes`, `uses_name`, ...).

## Progress export (schema 1)

`profile` (start date, placement, settings), `attempts[]` (one per exercise attempt: result, active seconds, runs,
hidden runs, hints, errors by type, final code), `mastery` (per-concept counts, SRS fields arrive in wave 2),
`modules` (status per module), `sessions[]` (one per day) and `events[]` (raw log, capped at 5 000). Import merges by
id and is idempotent. Attempts left mid-way are stored with `result: "left"`.

## Roadmap

Wave 1 (this): engine, L0 content, linear session, placement, export/import, PWA.
Wave 2: spaced repetition by concept, variants, checkpoints, tests-first and predict exercise types, scratch console,
L1 Toolbox (35 exercises), a separate profile for a second learner. Wave 3: L2 patterns. Wave 4: interview sprints with a
timer and L3 applied cases. See `docs/SPEC.md`.
