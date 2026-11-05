META = dict(
    id="l0.errors.group-with-setdefault", type="cloze", order=50,
    difficulty=1, minutes=2, world="bybit",
    concepts=["setdefault", "dict-basics"],
    story_en="Grouping trades by coin without the if-key-not-in-dict dance. Pixel calls that dance 'the beginner shuffle'.",
    title="Group with setdefault",
    statement_en="Fill in the dict method that returns the existing list for a key, or stores and returns a new empty list when the key is new.",
    hints_en=["dict.setdefault(key, default) returns the value for key, inserting default first if the key is missing."],
    hints_ru=["dict.setdefault(key, default) возвращает значение по ключу, предварительно вставив default, если ключа не было."],
    explanation_en="setdefault merges 'create if missing' and 'get' into one call, so grouping is a single line per item. collections.defaultdict(list) is the next step up.",
    explanation_ru="setdefault объединяет «создать, если нет» и «получить» в один вызов, поэтому группировка – одна строка на элемент. Следующий шаг – collections.defaultdict(list).",
)

STARTER = '''
trades = [("BTC", 1), ("ETH", 2), ("BTC", 3)]
by_symbol = {}
for symbol, qty in trades:
    by_symbol.___(symbol, []).append(qty)
# by_symbol == {"BTC": [1, 3], "ETH": [2]}
'''

SOLUTION = '''
trades = [("BTC", 1), ("ETH", 2), ("BTC", 3)]
by_symbol = {}
for symbol, qty in trades:
    by_symbol.setdefault(symbol, []).append(qty)
'''

TESTS = '''
def test_groups(ns, check):
    check(ns["by_symbol"], {"BTC": [1, 3], "ETH": [2]}, "by_symbol")

def test_uses_setdefault(src, ast_tools, check):
    check(ast_tools.count_calls(src, "setdefault") >= 1, True, "setdefault is used")
'''
