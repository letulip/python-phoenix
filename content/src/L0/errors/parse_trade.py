META = dict(
    id="l0.errors.parse-trade", type="task", order=68,
    difficulty=2, minutes=6, world="bybit",
    concepts=["raise", "value-error", "try-except"],
    story_en="Dr. Candle types his trades into a text file at night. 'btc, 0.5 ,Buy' is a good night. 'btc,lots,buy' is a bad night. The parser must tell them apart politely.",
    title="Parse a trade line",
    statement_en=("Write parse_trade(line) -> tuple. A line looks like 'BTC,0.5,buy': symbol, quantity and side separated "
                  "by commas, possibly with spaces around the fields, which must be stripped. Return (symbol upper-cased, "
                  "quantity as float, side lower-cased). Raise ValueError('expected 3 fields') when the number of "
                  "comma-separated fields is not 3, and ValueError('qty is not a number') when the quantity cannot be "
                  "converted to float."),
    hints_en=[
        "parts = [p.strip() for p in line.split(',')]; check len(parts) before touching the fields.",
        "Convert the quantity inside try/except ValueError and raise your own ValueError with the exact message.",
        "Return a tuple: symbol.upper(), qty, side.lower().",
    ],
    hints_ru=[
        "parts = [p.strip() for p in line.split(',')]; проверь len(parts) до обращения к полям.",
        "Конвертируй количество внутри try/except ValueError и бросай свой ValueError с точным сообщением.",
        "Верни кортеж: symbol.upper(), qty, side.lower().",
    ],
    explanation_en=("Validate the shape first (three fields), then the content (a number), and raise with messages that "
                    "say what the caller has to fix. Catching float's ValueError and raising your own turns a library "
                    "message into a domain message."),
    explanation_ru=("Сначала форма (три поля), потом содержимое (число), и raise с сообщениями, которые говорят, что чинить. "
                    "Поймать ValueError из float и бросить свой – значит превратить сообщение библиотеки в сообщение "
                    "предметной области."),
    talk_track=[
        "Say you validate shape before content and fail with precise messages.",
        "Mention you re-raise float's ValueError as a domain error, and what 'from None' would change.",
        "Complexity O(len(line)).",
    ],
    complexity="O(n) in the length of the line",
    followups=["Should 'BUY' and 'Sell' be accepted? What about 'hold'?", "How would you report the line number in a file of trades?"],
)

STARTER = '''
def parse_trade(line):
    ...
'''

EXAMPLES = [
    {"call": "parse_trade('btc, 0.5 ,Buy')", "expected": "('BTC', 0.5, 'buy')"},
]

SOLUTION = '''
def parse_trade(line):
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 3:
        raise ValueError("expected 3 fields")
    symbol, qty_text, side = parts
    try:
        qty = float(qty_text)
    except ValueError:
        raise ValueError("qty is not a number")
    return symbol.upper(), qty, side.lower()
'''

TESTS = '''
def test_happy_path(ns, check):
    check(ns["parse_trade"]("btc, 0.5 ,Buy"), ("BTC", 0.5, "buy"), "parse_trade('btc, 0.5 ,Buy')")

def test_returns_tuple(ns, check):
    check(type(ns["parse_trade"]("ETH,2,sell")), tuple, "type of the result")

def test_two_fields(ns, check, raises):
    check(str(raises(ValueError, ns["parse_trade"], "BTC,0.5")), "expected 3 fields", "two fields")

def test_four_fields(ns, check, raises):
    check(str(raises(ValueError, ns["parse_trade"], "BTC,0.5,buy,now")), "expected 3 fields", "four fields")

def test_bad_qty(ns, check, raises):
    check(str(raises(ValueError, ns["parse_trade"], "btc,lots,buy")), "qty is not a number", "qty 'lots'")

def test_integer_qty_becomes_float(ns, check):
    check(ns["parse_trade"]("SOL,3,SELL"), ("SOL", 3.0, "sell"), "qty 3 becomes 3.0")
'''

LEVELS = dict(
    middle=dict(
        code='''
def parse_trade(line):
    parts = line.split(",")
    if len(parts) != 3:
        raise ValueError("expected 3 fields")
    symbol = parts[0].strip().upper()
    side = parts[2].strip().lower()
    try:
        qty = float(parts[1].strip())
    except ValueError:
        raise ValueError("qty is not a number")
    return (symbol, qty, side)
''',
        note_en=("Split, count, convert, with the right exception class and the exact messages: it does the job. "
                 "parts[0], parts[1], parts[2] is positional access where unpacking would name the fields, and the "
                 "re-raise inside the except keeps the original ValueError chained as context, so the user of this "
                 "function sees two tracebacks for one bad number."),
        note_ru=("Разрезать, сосчитать, сконвертировать, с верным классом исключения и точными сообщениями: работу делает. "
                 "parts[0], parts[1], parts[2] – обращение по позиции там, где распаковка дала бы полям имена, а raise "
                 "внутри except оставляет исходный ValueError прицепленным как контекст, поэтому пользователь этой "
                 "функции видит два трейсбека на одно плохое число."),
    ),
    senior=dict(
        code='''
def parse_trade(line):
    """'symbol,qty,side' -> (SYMBOL, float qty, side) with the fields stripped."""
    try:
        symbol, qty_text, side = (part.strip() for part in line.split(","))
    except ValueError:
        raise ValueError("expected 3 fields") from None
    try:
        qty = float(qty_text)
    except ValueError:
        raise ValueError("qty is not a number") from None
    return symbol.upper(), qty, side.lower()
''',
        note_en=("Unpacking names the three fields and makes the count check free: the wrong number of fields is itself a "
                 "ValueError, caught and renamed. 'from None' cuts the chained traceback, because the caller cares about "
                 "'qty is not a number', not about float's internals. A senior says real code would return a NamedTuple "
                 "or dataclass, and asks which sides are valid instead of lower-casing blindly."),
        note_ru=("Распаковка называет три поля и делает проверку количества бесплатной: неверное число полей само по себе "
                 "ValueError, который ловится и переименовывается. from None обрезает цепочку трейсбеков, потому что "
                 "вызывающему важно «qty is not a number», а не внутренности float. Сеньор скажет, что настоящий код "
                 "вернул бы NamedTuple или dataclass, и спросит, какие стороны допустимы, вместо того чтобы вслепую "
                 "приводить к нижнему регистру."),
    ),
)
