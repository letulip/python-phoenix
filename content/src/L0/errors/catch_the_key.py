META = dict(
    id="l0.errors.catch-the-key", type="cloze", order=20,
    difficulty=1, minutes=2, world="bybit",
    concepts=["key-error", "try-except"],
    story_en="Dr. Candle keeps asking for coins that do not exist yet. The dictionary used to scream. Now it says zero.",
    title="Catch the key",
    statement_en="Fill in the exception class so that price_of('DOGE') returns 0 instead of crashing, while price_of('ETH') still returns 3500.",
    hints_en=["A missing dictionary key raises KeyError. Catch exactly that class."],
    hints_ru=["Отсутствующий ключ словаря бросает KeyError. Лови ровно этот класс."],
    explanation_en="prices[symbol] raises KeyError for an unknown key; catching that one class returns the fallback and still lets other errors through. prices.get(symbol, 0) would be the one-line alternative.",
    explanation_ru="prices[symbol] бросает KeyError для неизвестного ключа; ловля именно этого класса возвращает запасное значение и пропускает другие ошибки дальше. Однострочная альтернатива – prices.get(symbol, 0).",
)

STARTER = '''
prices = {"BTC": 68000, "ETH": 3500}

def price_of(symbol):
    try:
        return prices[symbol]
    except ___:
        return 0

# price_of("ETH") -> 3500,  price_of("DOGE") -> 0
'''

SOLUTION = '''
prices = {"BTC": 68000, "ETH": 3500}

def price_of(symbol):
    try:
        return prices[symbol]
    except KeyError:
        return 0
'''

TESTS = '''
def test_known(ns, check):
    check(ns["price_of"]("ETH"), 3500, "price_of('ETH')")

def test_unknown(ns, check):
    check(ns["price_of"]("DOGE"), 0, "price_of('DOGE')")

def test_catches_key_error_only(src, ast_tools, check):
    check(ast_tools.uses_name(src, "KeyError"), True, "except names KeyError")
'''
