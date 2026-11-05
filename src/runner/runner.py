"""Python Phoenix test harness.

Runs unchanged in two places:
  * inside Pyodide in the browser (loaded by src/runner/worker.js), and
  * in local CPython for the content gate (tools/build_content.py).

Only the standard library is used. Test functions declare the fixtures they
need by parameter name, pytest-style:

    def test_sorted_by_length(ns, check):
        check(ns["sort_words"](["bb", "a"]), ["a", "bb"], "sort_words(['bb', 'a'])")

Fixtures: ns (the learner's namespace after running their code), src (their
source text), stdout (what their code printed at import time), check, approx,
capture, raises, ast_tools.
"""

from __future__ import annotations

import ast
import contextlib
import inspect
import io
import json
import sys
import time
import traceback

STDOUT_LIMIT = 20_000
REPR_LIMIT = 400
USER_FILE = "<your code>"
TESTS_FILE = "<tests>"


# ----------------------------------------------------------------------------
# Fixtures available to tests
# ----------------------------------------------------------------------------

class CheckFailure(Exception):
    """Raised by check()/approx()/raises() when the learner's result is wrong."""

    def __init__(self, label, expected, actual):
        super().__init__(label)
        self.label = label
        self.expected = expected
        self.actual = actual


def short_repr(value):
    try:
        text = repr(value)
    except Exception as exc:  # pragma: no cover - defensive
        text = f"<unrepresentable {type(value).__name__}: {exc}>"
    return text if len(text) <= REPR_LIMIT else text[:REPR_LIMIT] + "…"


def _equal(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False


def check(actual, expected, label=""):
    """Assert actual == expected with a readable report."""
    if not _equal(actual, expected):
        raise CheckFailure(label, expected, actual)


def approx(actual, expected, label="", tol=1e-6):
    """Assert two numbers are equal within tol."""
    ok = isinstance(actual, (int, float)) and not isinstance(actual, bool) \
        and abs(actual - expected) <= tol
    if not ok:
        raise CheckFailure(label, expected, actual)


def capture(fn, *args, **kwargs):
    """Call fn and return everything it printed."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()


def raises(exc_type, fn, *args, **kwargs):
    """Assert that fn(*args, **kwargs) raises exc_type; return the exception."""
    label = f"raises {exc_type.__name__}"
    try:
        fn(*args, **kwargs)
    except exc_type as exc:
        return exc
    except Exception as exc:
        raise CheckFailure(label, exc_type.__name__, f"{type(exc).__name__}: {exc}")
    raise CheckFailure(label, exc_type.__name__, "no exception")


class AstTools:
    """Structural checks on the learner's source (for refactor tasks)."""

    @staticmethod
    def tree(src):
        return ast.parse(src)

    @staticmethod
    def count_calls(src, name):
        count = 0
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id == name:
                    count += 1
                elif isinstance(func, ast.Attribute) and func.attr == name:
                    count += 1
        return count

    @staticmethod
    def count_fstrings(src):
        """Top-level f-strings only: a format spec like {x:<10} is a nested
        JoinedStr in the AST and must not be counted."""
        tree = ast.parse(src)
        specs = {id(n.format_spec) for n in ast.walk(tree)
                 if isinstance(n, ast.FormattedValue) and n.format_spec is not None}
        return sum(1 for n in ast.walk(tree)
                   if isinstance(n, ast.JoinedStr) and id(n) not in specs)

    @staticmethod
    def function_names(src):
        return [n.name for n in ast.walk(ast.parse(src))
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    @staticmethod
    def count_nodes(src, *type_names):
        types = tuple(getattr(ast, t) for t in type_names)
        return sum(isinstance(n, types) for n in ast.walk(ast.parse(src)))

    @classmethod
    def has_for(cls, src):
        return cls.count_nodes(src, "For") > 0

    @classmethod
    def has_while(cls, src):
        return cls.count_nodes(src, "While") > 0

    @classmethod
    def has_loop(cls, src):
        return cls.count_nodes(src, "For", "While") > 0

    @classmethod
    def has_comprehension(cls, src):
        return cls.count_nodes(src, "ListComp", "DictComp", "SetComp", "GeneratorExp") > 0

    @classmethod
    def has_try(cls, src):
        return cls.count_nodes(src, "Try") > 0

    @classmethod
    def has_lambda(cls, src):
        return cls.count_nodes(src, "Lambda") > 0

    @classmethod
    def has_with(cls, src):
        return cls.count_nodes(src, "With") > 0

    @staticmethod
    def imports(src):
        names = set()
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split(".")[0])
        return names

    @staticmethod
    def uses_name(src, name):
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Name) and node.id == name:
                return True
            if isinstance(node, ast.Attribute) and node.attr == name:
                return True
        return False

    @staticmethod
    def is_recursive(src, name):
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.FunctionDef) and node.name == name:
                for inner in ast.walk(node):
                    if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name) \
                            and inner.func.id == name:
                        return True
        return False

    @staticmethod
    def body_lines(src):
        """Number of non-empty, non-comment lines."""
        return sum(1 for line in src.splitlines()
                   if line.strip() and not line.strip().startswith("#"))

    @staticmethod
    def max_duplicate_lines(src, min_len=12):
        """How many times the most repeated meaningful line appears."""
        seen = {}
        for line in src.splitlines():
            key = line.strip()
            if len(key) >= min_len and not key.startswith("#"):
                seen[key] = seen.get(key, 0) + 1
        return max(seen.values(), default=0)


ast_tools = AstTools()


# ----------------------------------------------------------------------------
# Running the learner's code
# ----------------------------------------------------------------------------

class LimitedIO(io.StringIO):
    """StringIO that stops recording after STDOUT_LIMIT characters."""

    def __init__(self):
        super().__init__()
        self.truncated = False

    def write(self, s):
        if self.truncated:
            return len(s)
        room = STDOUT_LIMIT - self.tell()
        if len(s) > room:
            super().write(s[:room])
            self.truncated = True
            return len(s)
        return super().write(s)


def format_error(exc, filename=USER_FILE):
    """Describe an exception with the line number inside the learner's code."""
    line = None
    if isinstance(exc, SyntaxError):
        if exc.filename == filename:
            line = exc.lineno
        message = exc.msg or str(exc)
    else:
        message = str(exc)
        for frame in traceback.extract_tb(exc.__traceback__):
            if frame.filename == filename:
                line = frame.lineno
    return {"type": type(exc).__name__, "message": message, "line": line}


def exec_user(code, filename=USER_FILE, out=None):
    ns = {"__name__": "__main__"}
    out = out if out is not None else LimitedIO()
    error = None
    with contextlib.redirect_stdout(out):
        try:
            exec(compile(code, filename, "exec"), ns)
        except BaseException as exc:  # noqa: BLE001 - we report everything
            error = format_error(exc, filename)
    return ns, out.getvalue(), error, out.truncated


def _normalize_output(text):
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def run_examples(ns, examples):
    """Evaluate the visible examples: [{"call": "f(1)", "expected": "2"}]
    or [{"call": "greet('Bob')", "prints": "Hi, Bob!"}]."""
    results = []
    for ex in examples:
        call = ex.get("call", "")
        item = {"call": call}
        try:
            if "prints" in ex:
                item["expected"] = ex["prints"]
                actual = capture(lambda: eval(call, ns))
                item["actual"] = actual.rstrip("\n")
                ok = _normalize_output(actual) == _normalize_output(ex["prints"])
            else:
                expected = eval(ex.get("expected", "None"), {"__builtins__": __builtins__})
                item["expected"] = short_repr(expected)
                actual = eval(call, ns)
                item["actual"] = short_repr(actual)
                ok = _equal(actual, expected)
            item["status"] = "pass" if ok else "fail"
        except BaseException as exc:  # noqa: BLE001
            item["status"] = "error"
            item["error"] = format_error(exc)
        results.append(item)
    return results


def run_code(code, examples=None):
    out = LimitedIO()
    ns, _, error, _ = exec_user(code, out=out)
    examples_out = []
    if error is None:
        with contextlib.redirect_stdout(out):  # prints inside the learner's functions stay visible
            examples_out = run_examples(ns, examples or [])
    ok = error is None and all(e["status"] == "pass" for e in examples_out)
    return {"ok": ok, "stdout": out.getvalue(), "truncated": out.truncated, "error": error,
            "examples": examples_out, "tests": []}


def _label_for(name, fn):
    doc = (fn.__doc__ or "").strip().splitlines()
    if doc:
        return doc[0]
    return name[5:].replace("_", " ") if name.startswith("test_") else name


def run_tests(code, tests_src):
    ns, stdout, error, truncated = exec_user(code)
    if error is not None:
        return {"ok": False, "stdout": stdout, "truncated": truncated, "error": error,
                "examples": [], "tests": []}

    tests_ns = {"check": check, "approx": approx, "capture": capture, "raises": raises,
                "ast_tools": ast_tools, "CheckFailure": CheckFailure}
    try:
        exec(compile(tests_src, TESTS_FILE, "exec"), tests_ns)
    except BaseException as exc:  # noqa: BLE001 - broken test file
        return {"ok": False, "stdout": stdout, "truncated": truncated,
                "error": {"type": "HarnessError", "message": f"tests failed to load: {exc}", "line": None},
                "examples": [], "tests": []}

    fixtures = {"ns": ns, "src": code, "stdout": stdout, "check": check, "approx": approx,
                "capture": capture, "raises": raises, "ast_tools": ast_tools}
    results = []
    for name, fn in list(tests_ns.items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        item = {"name": name, "label": _label_for(name, fn)}
        started = time.perf_counter()
        try:
            params = inspect.signature(fn).parameters
            missing = [p for p in params if p not in fixtures]
            if missing:
                raise RuntimeError(f"unknown fixture(s): {', '.join(missing)}")
            kwargs = {p: fixtures[p] for p in params}
            with contextlib.redirect_stdout(LimitedIO()):
                fn(**kwargs)
            item["status"] = "pass"
        except CheckFailure as cf:
            item["status"] = "fail"
            if cf.label:
                item["label"] = cf.label
            item["expected"] = short_repr(cf.expected)
            item["actual"] = short_repr(cf.actual)
        except AssertionError as exc:
            item["status"] = "fail"
            if str(exc):
                item["label"] = str(exc)
        except BaseException as exc:  # noqa: BLE001 - learner code blew up inside the test
            item["status"] = "error"
            item["error"] = format_error(exc)
        item["ms"] = round((time.perf_counter() - started) * 1000, 1)
        results.append(item)

    ok = bool(results) and all(r["status"] == "pass" for r in results)
    return {"ok": ok, "stdout": stdout, "truncated": truncated, "error": None,
            "examples": [], "tests": results}


# ----------------------------------------------------------------------------
# Scratch console (persistent namespace, REPL-like value echo)
# ----------------------------------------------------------------------------

_SCRATCH_NS = {"__name__": "__scratch__"}


def run_scratch(code, reset=False):
    global _SCRATCH_NS
    if reset:
        _SCRATCH_NS = {"__name__": "__scratch__"}
    out = LimitedIO()
    value = None
    error = None
    with contextlib.redirect_stdout(out):
        try:
            tree = ast.parse(code, USER_FILE)
            last_expr = None
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last_expr = ast.Expression(tree.body.pop().value)
            if tree.body:
                exec(compile(tree, USER_FILE, "exec"), _SCRATCH_NS)
            if last_expr is not None:
                result = eval(compile(last_expr, USER_FILE, "eval"), _SCRATCH_NS)
                if result is not None:
                    value = short_repr(result)
        except BaseException as exc:  # noqa: BLE001
            error = format_error(exc)
    return {"ok": error is None, "stdout": out.getvalue(), "truncated": out.truncated,
            "error": error, "value": value, "examples": [], "tests": []}


# ----------------------------------------------------------------------------
# Entry point used by the worker
# ----------------------------------------------------------------------------

def run_request(payload):
    req = json.loads(payload) if isinstance(payload, str) else payload
    kind = req.get("kind")
    started = time.perf_counter()
    if kind == "run":
        result = run_code(req.get("code", ""), req.get("examples") or [])
    elif kind == "tests":
        result = run_tests(req.get("code", ""), req.get("tests", ""))
    elif kind == "scratch":
        result = run_scratch(req.get("code", ""), bool(req.get("reset")))
    elif kind == "ping":
        result = {"ok": True, "python": sys.version.split()[0], "tests": [], "examples": []}
    else:
        result = {"ok": False, "error": {"type": "ProtocolError", "message": f"unknown kind {kind!r}", "line": None},
                  "tests": [], "examples": [], "stdout": ""}
    result["ms"] = round((time.perf_counter() - started) * 1000, 1)
    return json.dumps(result)
