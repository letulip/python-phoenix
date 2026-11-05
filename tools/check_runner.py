#!/usr/bin/env python3
"""Gate: the harness describes mismatches the UI can highlight (string, list, type, dict)."""
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("runner", ROOT / "src" / "runner" / "runner.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

CODE = """
def format_line(name, qty, price):
    return f"{name:<10} x {qty:>2}  {qty * price:>7.2f}"

def lines():
    return [format_line("tea", 2, 1.5), "milk"]

def total():
    return "3"

def counts():
    return {"tea": 2, "jam": 1}
"""

TESTS = """
def test_line(ns, check):
    check(ns["format_line"]("tea", 2, 1.5), "tea        x 2     3.00", "line")

def test_lines(ns, check):
    check(ns["lines"](), ["tea        x 2     3.00", "milk"], "lines")

def test_total(ns, check):
    check(ns["total"](), 3, "total")

def test_counts(ns, check):
    check(ns["counts"](), {"tea": 2, "milk": 1}, "counts")
"""

EXAMPLES = [{"call": "format_line('tea', 2, 1.5)", "expected": "'tea        x 2     3.00'"},
            {"call": "print(format_line('tea', 2, 1.5))", "prints": "tea        x 2     3.00"}]


def expect(cond, message):
    if not cond:
        print("check_runner: FAIL -", message)
        sys.exit(1)


res = runner.run_tests(CODE, TESTS)
json.dumps(res)  # the worker ships it as JSON
by_name = {t["name"]: t for t in res["tests"]}

m = by_name["test_line"]["mismatch"]
expect(m["kind"] == "str" and m["elen"] == 23 and m["alen"] == 24 and m["pos"] == 13, f"str: {m}")
m = by_name["test_lines"]["mismatch"]
expect(m["kind"] == "seq" and m["pos"] == 0 and m["ndiff"] == 1 and m["items"][0]["pos"] == 13
       and m["items"][0]["alen"] == 24 and m["items"][0]["index"] == 0, f"seq: {m}")
m = by_name["test_total"]["mismatch"]
expect(m["etype"] == "int" and m["atype"] == "str" and m["kind"] == "other", f"type: {m}")
m = by_name["test_counts"]["mismatch"]
expect(m["kind"] == "dict" and m["missing"] == ["'milk'"] and m["extra"] == ["'jam'"] and m["changed"] == [], f"dict: {m}")

ex = runner.run_code(CODE, EXAMPLES)["examples"]
json.dumps(ex)
expect(ex[0]["status"] == "fail" and ex[0]["mismatch"]["kind"] == "str" and ex[0]["mismatch"]["pos"] == 13, f"example: {ex[0]}")
expect(ex[1]["status"] == "fail" and ex[1]["mismatch"]["pos"] == 13 and ex[1]["actual"].count(" ") == 15, f"prints example: {ex[1]}")
print("check_runner: OK")
