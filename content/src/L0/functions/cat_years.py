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

LEVELS = dict(
    middle=dict(
        note_en=("Correct and easy to read: the special years come first, the formula last, every branch returns. "
                 "An interviewer would still point at the magic numbers 15, 9 and 4 living inside the logic, at the "
                 "case for 2 that the formula already covers, and at a negative input that quietly returns nonsense."),
        note_ru=("Верно и читается легко: особые годы сначала, формула в конце, каждая ветка возвращает. "
                 "Интервьюер всё же укажет на магические числа 15, 9 и 4 внутри логики, на отдельный случай для 2, "
                 "который формула и так покрывает, и на отрицательный вход, который тихо возвращает чепуху."),
    ),
    senior=dict(
        code='''
FIRST_YEAR, SECOND_YEAR, EACH_LATER_YEAR = 15, 9, 4

def cat_age(human_years):
    """Cat years: 15 for the first human year, 9 for the second, 4 for each one after."""
    if human_years < 0:
        raise ValueError("human_years must not be negative")
    if human_years == 0:
        return 0
    if human_years == 1:
        return FIRST_YEAR
    return FIRST_YEAR + SECOND_YEAR + EACH_LATER_YEAR * (human_years - 2)
''',
        note_en=("Before typing, a senior asks what a negative input means and makes it fail loudly instead of guessing. "
                 "The rates get names in one place, so the follow-up about configurable constants is already answered, "
                 "and the docstring states the rule the tests check. The clever one-liner with sum() is avoided on purpose: "
                 "shorter is not the goal, obvious is."),
        note_ru=("Прежде чем печатать, сеньор спрашивает, что значит отрицательный вход, и делает так, чтобы он падал громко, "
                 "а не угадывал. Ставки названы и лежат в одном месте, так что вопрос про настраиваемые константы уже закрыт; "
                 "докстринг формулирует правило, которое проверяют тесты. Хитрая однострочка с sum() отброшена сознательно: "
                 "цель не короче, а очевиднее."),
    ),
)
