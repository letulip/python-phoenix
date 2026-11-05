META = dict(
    id="l0.functions.cat-years", type="task", order=60,
    difficulty=1, minutes=5, world="everyday",
    concepts=["def-return", "early-return", "call-function"],
    story_en="Pixel's birthday card must say the right age, or the card goes under the sofa with the other mistakes.",
    title="Cat years",
    statement_en=("Pixel the cat demands a birthday card in cat years. Write cat_age(human_years) -> int. "
                  "The first human year counts as 15 cat years, the second adds 9, and every year after that adds 4. "
                  "Zero human years is zero cat years. human_years is a non-negative int."),
    hints_en=[
        "Handle the small cases first: 0 -> 0, 1 -> 15, 2 -> 24. Each gets its own early return.",
        "For human_years > 2 the answer is 24 + 4 * (human_years - 2).",
        "Three ifs with returns, then one return with the formula. No else needed.",
    ],
    hints_ru=[
        "Сначала разберись с маленькими случаями: 0 -> 0, 1 -> 15, 2 -> 24. Каждому – свой ранний return.",
        "Для human_years > 2 ответ 24 + 4 * (human_years - 2).",
        "Три if с return, затем один return с формулой. else не нужен.",
    ],
    explanation_en=("Special cases first, general formula last: the reader sees the exceptions and then the rule. "
                    "Because every branch returns, no else chain is needed."),
    explanation_ru=("Сначала особые случаи, в конце общая формула: читатель видит исключения, потом правило. "
                    "Каждая ветка возвращает значение, поэтому цепочка else не нужна."),
    talk_track=[
        "Restate: piecewise formula with two special years.",
        "Call out the edge case zero before writing code.",
        "Say the function is O(1) and has no loops.",
    ],
    complexity="O(1)",
    followups=["What should happen for a negative input?", "How would you make the 15/9/4 constants configurable?"],
)

STARTER = '''
def cat_age(human_years):
    ...
'''

EXAMPLES = [
    {"call": "cat_age(1)", "expected": "15"},
    {"call": "cat_age(3)", "expected": "28"},
    {"call": "cat_age(0)", "expected": "0"},
]

SOLUTION = '''
def cat_age(human_years):
    if human_years == 0:
        return 0
    if human_years == 1:
        return 15
    if human_years == 2:
        return 24
    return 24 + 4 * (human_years - 2)
'''

SOLUTION_ALT = '''
def cat_age(human_years):
    steps = [15, 9]
    return sum(steps[:human_years]) + 4 * max(0, human_years - 2)
'''

TESTS = '''
def test_zero(ns, check):
    check(ns["cat_age"](0), 0, "cat_age(0)")

def test_first_year(ns, check):
    check(ns["cat_age"](1), 15, "cat_age(1)")

def test_second_year(ns, check):
    check(ns["cat_age"](2), 24, "cat_age(2)")

def test_third_year(ns, check):
    check(ns["cat_age"](3), 28, "cat_age(3)")

def test_ten_years(ns, check):
    check(ns["cat_age"](10), 56, "cat_age(10)")

def test_returns_int(ns, check):
    check(type(ns["cat_age"](7)), int, "type(cat_age(7))")
'''
