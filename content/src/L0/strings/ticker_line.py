META = dict(
    id="l0.strings.ticker-line", type="refactor", order=90,
    difficulty=2, minutes=6, world="bybit",
    concepts=["f-string", "format-spec", "str-methods"],
    story_en="Dr. Candle's ticker is glued together from pieces with + and %, padded by hand. It lines up. Nobody dares to touch it. Today, you dare.",
    title="Ticker line with f-strings",
    statement_en=("ticker_line(symbol, price, change) returns one aligned ticker row and works, but it is built from + "
                  "concatenation, old %-formatting and hand-made padding with len. Rewrite it as a single f-string with "
                  "format specs: symbol left-aligned in 6, price right-aligned in 10 with 2 decimals, two spaces, "
                  "change with an explicit sign and 1 decimal, then '%'. No %, no len() and no + on strings may remain. "
                  "Output must not change."),
    hints_en=[
        "Left alignment is {symbol:<6}; right alignment with decimals is {price:>10.2f}.",
        "A sign on positive numbers too is the + flag: {change:+.1f}.",
        "The literal percent sign is just a character after the braces: f'...{change:+.1f}%'.",
    ],
    hints_ru=[
        "Выравнивание влево – {symbol:<6}; вправо с десятичными – {price:>10.2f}.",
        "Знак и у положительных чисел – флаг +: {change:+.1f}.",
        "Сам знак процента – просто символ после скобок: f'...{change:+.1f}%'.",
    ],
    explanation_en=("Format specs do alignment, width, precision and sign in one place, so the padding arithmetic and the "
                    "sign branch disappear. One f-string also shows the shape of the row at a glance, which the "
                    "concatenation version never could."),
    explanation_ru=("Спецификаторы формата делают выравнивание, ширину, точность и знак в одном месте, поэтому арифметика "
                    "отступов и ветка со знаком исчезают. Одна f-строка ещё и показывает форму строки с первого взгляда, "
                    "чего версия со склейкой не могла никогда."),
    talk_track=[
        "Say the format spec encodes width, alignment, precision and sign, so no manual padding is needed.",
        "Mention the + flag prints the sign for positive numbers too.",
    ],
    complexity="O(1)",
    followups=["How would you format thousands separators? Python has a flag for that.", "What should happen if a symbol is longer than 6 characters?"],
)

STARTER = '''
def ticker_line(symbol, price, change):
    padded = symbol + " " * (6 - len(symbol))
    price_text = "%.2f" % price
    price_text = " " * (10 - len(price_text)) + price_text
    sign = "+" if change >= 0 else ""
    return padded + price_text + "  " + sign + "%.1f" % change + "%"
'''

EXAMPLES = [
    {"call": "ticker_line('BTC', 68000, 1.5)", "expected": "'BTC     68000.00  +1.5%'"},
    {"call": "ticker_line('ETH', 3500.123, -2.25)", "expected": "'ETH      3500.12  -2.2%'"},
]

SOLUTION = '''
def ticker_line(symbol, price, change):
    return f"{symbol:<6}{price:>10.2f}  {change:+.1f}%"
'''

TESTS = '''
def test_positive_change(ns, check):
    check(ns["ticker_line"]("BTC", 68000, 1.5), "BTC     68000.00  +1.5%", "ticker_line('BTC', 68000, 1.5)")

def test_negative_change(ns, check):
    check(ns["ticker_line"]("ETH", 3500.123, -2.25), "ETH      3500.12  -2.2%", "ticker_line('ETH', 3500.123, -2.25)")

def test_zero_change(ns, check):
    check(ns["ticker_line"]("DOGE", 0.1, 0), "DOGE        0.10  +0.0%", "zero change keeps the plus sign")

def test_width(ns, check):
    check(len(ns["ticker_line"]("SOL", 150, 3)), 23, "the row is 23 characters wide")

def test_uses_fstring_only(src, ast_tools, check):
    check(ast_tools.count_fstrings(src) >= 1, True, "an f-string is used")
    check(ast_tools.count_nodes(src, "Mod"), 0, "no %-formatting left")
    check(ast_tools.count_calls(src, "len"), 0, "no len() padding left")
    check(ast_tools.count_nodes(src, "Add"), 0, "no + concatenation left")
'''

LEVELS = dict(
    middle=dict(
        note_en=("One f-string with three format specs: exactly the refactor asked for, and the output is identical. A "
                 "reviewer has nothing to fix here; what they might ask is what the function promises when the symbol is "
                 "longer than six characters, because the alignment silently breaks and the code does not say so."),
        note_ru=("Одна f-строка с тремя спецификаторами: ровно тот рефакторинг, который просили, и вывод идентичен. "
                 "Ревьюеру чинить нечего; спросить он может лишь, что функция обещает, когда тикер длиннее шести символов, "
                 "потому что выравнивание тихо ломается, а код об этом молчит."),
    ),
    senior=dict(
        code='''
SYMBOL_WIDTH, PRICE_WIDTH = 6, 10

def ticker_line(symbol, price, change):
    """One aligned ticker row; a symbol longer than SYMBOL_WIDTH pushes the price right."""
    return f"{symbol:<{SYMBOL_WIDTH}}{price:>{PRICE_WIDTH}.2f}  {change:+.1f}%"
''',
        note_en=("Same f-string, but the widths are named constants and the specs take them as nested fields, so the "
                 "layout is one place to change and the docstring states the known limit instead of hiding it. A senior "
                 "mentions the thousands-separator flag ({price:>12,.2f}) and that a real ticker would take a dataclass, "
                 "not three loose arguments, and leaves both for the follow-up."),
        note_ru=("Та же f-строка, но ширины – именованные константы, а спецификаторы берут их вложенными полями, так что "
                 "раскладка меняется в одном месте, а докстринг называет известный предел, а не прячет его. Сеньор "
                 "упомянет флаг разделителя тысяч ({price:>12,.2f}) и то, что настоящий тикер принимал бы dataclass, а не "
                 "три отдельных аргумента, и оставит оба пункта на дополнительный вопрос."),
    ),
)
