META = dict(
    id="l0.errors.robust-average", type="task", order=60,
    difficulty=2, minutes=6, world="bybit",
    concepts=["try-except", "value-error", "sum", "eafp-lbyl"],
    story_en="Dr. Candle's feed at 3 a.m.: '68000', 'n/a', '67950', 'reconnecting...'. The average must still come out.",
    title="Robust average",
    statement_en=("Write average_price(values) -> float | None. values is a list of strings from a price feed. Convert each "
                  "to a float with try/except, skipping the ones that are not valid numbers. Return the average of the valid "
                  "ones rounded to 2 decimals, or None when there are no valid numbers."),
    hints_en=[
        "Wrap float(text) in try/except ValueError and skip the bad ones with continue.",
        "Collect the valid floats in a list; if that list is empty, return None before dividing.",
        "round(sum(valid) / len(valid), 2) is the answer.",
    ],
    hints_ru=[
        "Оберни float(text) в try/except ValueError и пропускай плохие через continue.",
        "Собирай валидные float в список; если список пуст, верни None до деления.",
        "Ответ – round(sum(valid) / len(valid), 2).",
    ],
    explanation_en=("EAFP beats inspection here: float() already knows every valid spelling, including '-1' and '1e3', which "
                    "an isdigit check would reject. Handling the empty case first avoids ZeroDivisionError."),
    explanation_ru=("Здесь EAFP лучше проверок: float() уже знает все допустимые записи, включая '-1' и '1e3', которые "
                    "отверг бы isdigit. Обработка пустого случая первой избавляет от ZeroDivisionError."),
    talk_track=[
        "Say EAFP: try to convert, catch ValueError, skip; it accepts '-1' and '1e3' that isdigit would reject.",
        "Mention the empty case first: the average of nothing is None, not a ZeroDivisionError.",
        "Complexity O(n).",
    ],
    complexity="O(n)",
    followups=["Should 'nan' and 'inf' count as valid? float accepts them.", "How would you also report how many values were skipped?"],
)

STARTER = '''
def average_price(values):
    ...
'''

EXAMPLES = [
    {"call": "average_price(['1.5', '2.5'])", "expected": "2.0"},
    {"call": "average_price(['n/a', '3'])", "expected": "3.0"},
    {"call": "average_price([])", "expected": "None"},
]

SOLUTION = '''
def average_price(values):
    valid = []
    for text in values:
        try:
            valid.append(float(text))
        except ValueError:
            continue
    if not valid:
        return None
    return round(sum(valid) / len(valid), 2)
'''

TESTS = '''
def test_simple(ns, check):
    check(ns["average_price"](["1.5", "2.5"]), 2.0, "average_price(['1.5', '2.5'])")

def test_skips_garbage(ns, check):
    check(ns["average_price"](["n/a", "3", "reconnecting..."]), 3.0, "garbage skipped")

def test_empty(ns, check):
    check(ns["average_price"]([]), None, "average_price([])")

def test_all_garbage(ns, check):
    check(ns["average_price"](["a", "b"]), None, "nothing valid")

def test_rounding(ns, check):
    check(ns["average_price"](["1", "2", "4"]), 2.33, "rounded to 2 decimals")

def test_negative_and_scientific(ns, check):
    check(ns["average_price"](["-1", "3", "1e1"]), 4.0, "'-1' and '1e1' are valid floats")

def test_uses_try(src, ast_tools, check):
    check(ast_tools.has_try(src), True, "uses try/except")
'''
