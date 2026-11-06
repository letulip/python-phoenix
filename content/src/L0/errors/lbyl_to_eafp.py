META = dict(
    id="l0.errors.lbyl-to-eafp", type="refactor", order=90,
    difficulty=2, minutes=6, world="bybit",
    concepts=["eafp-lbyl", "try-except", "dict-get"],
    story_en="The bot's old helpers peek before every move: is it a digit, is the key there. They miss negative prices and every wallet lookup is written twice. Pixel calls it 'asking permission from a string'.",
    title="From look-before-you-leap to EAFP",
    statement_en=("Both functions inspect before acting: to_cents checks the text with isdigit before converting, "
                  "balance_of checks 'name in wallets' before reading. Rewrite them in the EAFP style: to_cents tries "
                  "float() and returns None on ValueError; balance_of uses dict.get with a default of 0. No isdigit and "
                  "no if statement may remain, and to_cents must accept every text float() accepts, including '-1.50' "
                  "and '1e2'."),
    hints_en=[
        "to_cents: try: return round(float(text) * 100) except ValueError: return None.",
        "balance_of: wallets.get(name, 0) is the whole body.",
        "Delete the isdigit line entirely; float() already knows what a number looks like.",
    ],
    hints_ru=[
        "to_cents: try: return round(float(text) * 100) except ValueError: return None.",
        "balance_of: wallets.get(name, 0) – это всё тело функции.",
        "Строку с isdigit удали целиком; float() и так знает, как выглядит число.",
    ],
    explanation_en=("Inspecting a string by hand re-implements float() badly: isdigit rejects '-1.50' and '1e2' that "
                    "float accepts. Trying the conversion and catching ValueError delegates the definition of 'number' "
                    "to the one place that owns it. dict.get collapses 'check then read' into one lookup."),
    explanation_ru=("Проверка строки вручную плохо переизобретает float(): isdigit отвергает '-1.50' и '1e2', которые "
                    "float принимает. Попытка конвертации с ловлей ValueError отдаёт определение «числа» тому "
                    "единственному месту, которое им владеет. dict.get сворачивает «проверь, потом прочитай» в одно обращение."),
    talk_track=[
        "Say isdigit was a worse float() and name the inputs it rejected.",
        "Mention dict.get does the check and the read in one lookup instead of two.",
    ],
    complexity="O(1)",
    followups=["Why is float the wrong type for money, and what would you use?", "What does round() do with 0.5? Is that what the bot wants?"],
)

STARTER = '''
def to_cents(text):
    if text.replace(".", "", 1).isdigit():
        return round(float(text) * 100)
    return None

def balance_of(wallets, name):
    if name in wallets:
        return wallets[name]
    return 0
'''

EXAMPLES = [
    {"call": "to_cents('12.34')", "expected": "1234"},
    {"call": "to_cents('n/a')", "expected": "None"},
    {"call": "balance_of({'ada': 50}, 'byte')", "expected": "0"},
]

SOLUTION = '''
def to_cents(text):
    try:
        return round(float(text) * 100)
    except ValueError:
        return None

def balance_of(wallets, name):
    return wallets.get(name, 0)
'''

TESTS = '''
def test_plain_number(ns, check):
    check(ns["to_cents"]("12.34"), 1234, "to_cents('12.34')")

def test_negative_and_scientific(ns, check):
    check((ns["to_cents"]("-1.50"), ns["to_cents"]("1e2")), (-150, 10000), "'-1.50' and '1e2' are numbers")

def test_not_a_number(ns, check):
    check(ns["to_cents"]("n/a"), None, "to_cents('n/a')")

def test_balance(ns, check):
    wallets = {"ada": 50}
    check((ns["balance_of"](wallets, "ada"), ns["balance_of"](wallets, "byte")), (50, 0), "known and unknown wallet")

def test_eafp_style(src, ast_tools, check):
    check(ast_tools.has_try(src), True, "to_cents uses try/except")
    check(ast_tools.count_calls(src, "isdigit"), 0, "no isdigit left")
    check(ast_tools.count_nodes(src, "If"), 0, "no if statements left")
    check(ast_tools.count_calls(src, "get") >= 1, True, "balance_of uses dict.get")
'''

LEVELS = dict(
    middle=dict(
        note_en=("EAFP done right: try the conversion, catch the one expected failure, return the sentinel, and dict.get "
                 "for the lookup. The one habit a reviewer flags: the try block wraps the multiplication and the "
                 "rounding too, not only the call that can fail, and that habit later hides real bugs behind an except."),
        note_ru=("EAFP как надо: попробовать конвертацию, поймать единственный ожидаемый сбой, вернуть сторожевое значение, "
                 "и dict.get для поиска. Единственная привычка, которую отметит ревьюер: блок try обёртывает ещё и "
                 "умножение с округлением, а не только вызов, который может упасть, и позже эта привычка прячет настоящие "
                 "баги за except."),
    ),
    senior=dict(
        code='''
def to_cents(text):
    """Whole cents for a decimal text, or None when it is not a number."""
    try:
        amount = float(text)
    except ValueError:
        return None
    return round(amount * 100)

def balance_of(wallets, name):
    return wallets.get(name, 0)
''',
        note_en=("The try covers exactly the one line that can fail; the arithmetic sits outside, so a bug in it is never "
                 "mistaken for bad input. A senior then says the two things the exercise does not: float is the wrong "
                 "type for money (Decimal is the honest one) and round() rounds halves to even, and raises both with the "
                 "interviewer instead of silently 'fixing' them."),
        note_ru=("try накрывает ровно одну строку, которая может упасть; арифметика снаружи, поэтому ошибку в ней никогда "
                 "не примут за плохой ввод. Дальше сеньор говорит две вещи, которых упражнение не говорит: float – "
                 "неверный тип для денег (честный – Decimal), а round() округляет половинки к чётному, и поднимает обе "
                 "темы с интервьюером вместо того, чтобы молча «починить»."),
    ),
)
