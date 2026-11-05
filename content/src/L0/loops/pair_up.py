META = dict(
    id="l0.loops.pair-up", type="cloze", order=30,
    difficulty=1, minutes=3, world="everyday",
    concepts=["zip", "for-loop", "dict-basics"],
    story_en="Grandma Ada wrote the names on one list and the prices on another. Grandma Ada is testing you.",
    title="Pair up names and prices",
    statement_en="Fill in the blanks: walk both lists together to build price_of, then collect the names cheaper than 5.",
    hints_en=["zip(names, prices) yields (name, price) pairs. Cheaper than 5 is the < operator."],
    hints_ru=["zip(names, prices) выдаёт пары (name, price). Дешевле 5 – это оператор <."],
    explanation_en="zip pairs items by position and stops at the shorter list, so you never index two lists in parallel by hand.",
    explanation_ru="zip соединяет элементы по позиции и останавливается на более коротком списке, поэтому два списка не нужно индексировать параллельно вручную.",
)

STARTER = '''
names = ["rope", "lamp", "map"]
prices = [3, 12, 7]
price_of = {}
for name, price in ___(names, prices):
    price_of[name] = price

cheap = []
for name, price in price_of.items():
    if price ___ 5:
        cheap.append(name)
# price_of == {"rope": 3, "lamp": 12, "map": 7}, cheap == ["rope"]
'''

SOLUTION = '''
names = ["rope", "lamp", "map"]
prices = [3, 12, 7]
price_of = {}
for name, price in zip(names, prices):
    price_of[name] = price

cheap = []
for name, price in price_of.items():
    if price < 5:
        cheap.append(name)
'''

TESTS = '''
def test_price_of(ns, check):
    check(ns["price_of"], {"rope": 3, "lamp": 12, "map": 7}, "price_of")

def test_cheap(ns, check):
    check(ns["cheap"], ["rope"], "cheap")

def test_uses_zip(src, ast_tools, check):
    check(ast_tools.uses_name(src, "zip"), True, "zip is used")
'''
