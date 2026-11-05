META = dict(
    id="l0.errors.safe-parse", type="retype", order=10,
    difficulty=1, minutes=3, world="bybit",
    concepts=["try-except", "value-error", "index-error"],
    story_en="Dr. Candle's feed sends 'n/a' at 3 a.m. The bot used to sink at 3 a.m. Now it shrugs.",
    title="Safe parse",
    statement_en="Retype both functions: each tries the risky operation and returns a fallback for exactly one expected exception.",
    hints_en=["float('n/a') raises ValueError; [][0] raises IndexError. The except line names the class without quotes."],
    hints_ru=["float('n/a') бросает ValueError; [][0] бросает IndexError. Строка except называет класс без кавычек."],
    explanation_en="This is EAFP: try the operation, catch the one failure you expect, return a fallback. Catching the specific class keeps real bugs (a typo, a None) visible.",
    explanation_ru="Это EAFP: попробуй операцию, поймай единственный ожидаемый сбой, верни запасное значение. Ловля конкретного класса оставляет настоящие баги (опечатку, None) на виду.",
)

MODEL = '''
def parse_price(text):
    try:
        return float(text)
    except ValueError:
        return None

def first_or_default(items, default="none"):
    try:
        return items[0]
    except IndexError:
        return default
'''

STARTER = ""

TESTS = '''
def test_parse_valid(ns, check):
    check((ns["parse_price"]("3.5"), ns["parse_price"]("42")), (3.5, 42.0), "parse_price on valid text")

def test_parse_invalid(ns, check):
    check(ns["parse_price"]("n/a"), None, "parse_price('n/a')")

def test_first_or_default(ns, check):
    check((ns["first_or_default"]([]), ns["first_or_default"]([7])), ("none", 7), "first_or_default")

def test_custom_default(ns, check):
    check(ns["first_or_default"]([], default=0), 0, "first_or_default([], default=0)")
'''
