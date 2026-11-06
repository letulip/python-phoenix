META = dict(
    id="l0.errors.validate-order", type="task", order=70,
    difficulty=3, minutes=8, world="bybit",
    concepts=["raise", "value-error", "dict-get", "key-error"],
    story_en="Dr. Candle's bot once bought minus two BTC of a coin named ''. The exchange was confused. So was Dr. Candle.",
    title="Validate an order",
    statement_en=("Write validate_order(order) -> dict. order is a dict that should contain 'symbol' (a non-empty str), 'qty' "
                  "(an int or float greater than 0, and not a bool) and 'side' ('buy' or 'sell' in any letter case). Check in "
                  "that order and raise ValueError with exactly these messages: 'symbol is required', 'qty must be positive', "
                  "'side must be buy or sell'. Return a new dict {'symbol': symbol upper-cased, 'qty': float(qty), 'side': side "
                  "lower-cased} and do not modify the input."),
    hints_en=[
        "Read with order.get(key) so a missing key becomes None instead of KeyError, then validate the value.",
        "Raise ValueError('message') as soon as a check fails; the order is symbol, qty, side.",
        "Normalise at the end: symbol.upper(), float(qty), side.lower(); build and return a new dict.",
    ],
    hints_ru=[
        "Читай через order.get(key), чтобы отсутствующий ключ стал None, а не KeyError, затем проверяй значение.",
        "Бросай ValueError('message'), как только проверка не прошла; порядок: symbol, qty, side.",
        "Нормализуй в конце: symbol.upper(), float(qty), side.lower(); собери и верни новый словарь.",
    ],
    explanation_en=("Validate in a fixed order and fail fast with a precise message, so the caller knows what to fix first. "
                    "bool is a subclass of int, so isinstance(True, int) is True: exclude it explicitly. Returning a new dict "
                    "keeps the function pure."),
    explanation_ru=("Проверяй в фиксированном порядке и падай быстро с точным сообщением, чтобы вызывающий знал, что чинить "
                    "первым. bool – подкласс int, поэтому isinstance(True, int) истинно: исключай его явно. Новый словарь на "
                    "выходе сохраняет функцию чистой."),
    talk_track=[
        "Say you validate in a fixed order and fail fast with precise messages.",
        "Mention .get avoids KeyError, so missing and empty are handled by one check.",
        "Point out that bool is an int subclass and needs an explicit exclusion.",
    ],
    complexity="O(1)",
    followups=["How would you collect every problem instead of raising at the first?", "Would a dataclass with __post_init__ be a better home for these rules?"],
)

STARTER = '''
def validate_order(order):
    ...
'''

EXAMPLES = [
    {"call": "validate_order({'symbol': 'btc', 'qty': 2, 'side': 'Buy'})", "expected": "{'symbol': 'BTC', 'qty': 2.0, 'side': 'buy'}"},
]

SOLUTION = '''
def validate_order(order):
    symbol = order.get("symbol")
    if not isinstance(symbol, str) or not symbol:
        raise ValueError("symbol is required")
    qty = order.get("qty")
    if isinstance(qty, bool) or not isinstance(qty, (int, float)) or qty <= 0:
        raise ValueError("qty must be positive")
    side = order.get("side")
    if not isinstance(side, str) or side.lower() not in ("buy", "sell"):
        raise ValueError("side must be buy or sell")
    return {"symbol": symbol.upper(), "qty": float(qty), "side": side.lower()}
'''

TESTS = '''
def test_happy_path(ns, check):
    check(ns["validate_order"]({"symbol": "btc", "qty": 2, "side": "Buy"}),
          {"symbol": "BTC", "qty": 2.0, "side": "buy"}, "normalised order")

def test_missing_symbol(ns, check, raises):
    check(str(raises(ValueError, ns["validate_order"], {"qty": 1, "side": "buy"})), "symbol is required", "missing symbol")

def test_empty_symbol(ns, check, raises):
    check(str(raises(ValueError, ns["validate_order"], {"symbol": "", "qty": 1, "side": "buy"})), "symbol is required", "empty symbol")

def test_bad_qty(ns, check, raises):
    for qty in (0, -1, "2", None, True):
        check(str(raises(ValueError, ns["validate_order"], {"symbol": "ETH", "qty": qty, "side": "sell"})),
              "qty must be positive", f"qty={qty!r}")

def test_bad_side(ns, check, raises):
    check(str(raises(ValueError, ns["validate_order"], {"symbol": "ETH", "qty": 1, "side": "hold"})), "side must be buy or sell", "side hold")
    check(str(raises(ValueError, ns["validate_order"], {"symbol": "ETH", "qty": 1})), "side must be buy or sell", "side missing")

def test_check_order(ns, check, raises):
    check(str(raises(ValueError, ns["validate_order"], {"qty": 0})), "symbol is required", "symbol is checked first")

def test_input_untouched(ns, check):
    order = {"symbol": "eth", "qty": 1.5, "side": "SELL"}
    out = ns["validate_order"](order)
    check(out, {"symbol": "ETH", "qty": 1.5, "side": "sell"}, "sell order")
    check(order, {"symbol": "eth", "qty": 1.5, "side": "SELL"}, "input dict unchanged")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Fixed order, fail fast, precise messages, bool excluded, a new dict returned: everything the statement "
                 "asked for, and the hard parts (bool is an int, .get instead of KeyError) are handled. The three "
                 "if/raise pairs are the same shape repeated, which is the first thing a reviewer circles."),
        note_ru=("Фиксированный порядок, быстрое падение, точные сообщения, bool исключён, возвращается новый словарь: всё, "
                 "что просило условие, и сложные места (bool – это int, .get вместо KeyError) закрыты. Три пары if/raise – "
                 "одна и та же форма трижды, и ревьюер обведёт это первым."),
    ),
    senior=dict(
        code='''
SIDES = ("buy", "sell")

def _require(condition, message):
    if not condition:
        raise ValueError(message)

def validate_order(order):
    """Normalised copy of `order`; ValueError with a precise message on the first broken rule."""
    symbol, qty, side = order.get("symbol"), order.get("qty"), order.get("side")
    _require(isinstance(symbol, str) and symbol, "symbol is required")
    _require(isinstance(qty, (int, float)) and not isinstance(qty, bool) and qty > 0, "qty must be positive")
    _require(isinstance(side, str) and side.lower() in SIDES, "side must be buy or sell")
    return {"symbol": symbol.upper(), "qty": float(qty), "side": side.lower()}
''',
        note_en=("The repeated if-not-condition-raise becomes one helper, so each rule is a single readable line with its "
                 "message beside it, and the allowed sides are a named constant. A senior says that in a real codebase "
                 "these rules belong to a dataclass or a pydantic model validated at the boundary, and that collecting "
                 "all errors instead of stopping at the first is a product decision to ask about, not to assume."),
        note_ru=("Повторяющееся «если не условие – raise» стало одним помощником, поэтому каждое правило – одна читаемая "
                 "строка с сообщением рядом, а допустимые стороны – именованная константа. Сеньор скажет, что в настоящем "
                 "коде эти правила живут в dataclass или модели pydantic с валидацией на границе, а собирать все ошибки "
                 "вместо остановки на первой – продуктовое решение, о котором спрашивают, а не предполагают."),
    ),
)
