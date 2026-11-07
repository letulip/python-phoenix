META = dict(
    id="gym.enumerate-zip.dict-from-zip", type="cloze", order=40,
    difficulty=1, minutes=1, world="everyday",
    concepts=["zip", "dict-basics"],
    title="A dict from two lists",
    statement_en="Fill in the built-in that pairs the keys with the values so that dict() can build the table.",
    hints_en=["zip(keys, values) yields (key, value) pairs, which is exactly what dict() wants."],
    hints_ru=["zip(keys, values) выдаёт пары (ключ, значение), а это ровно то, чего ждёт dict()."],
    explanation_en="dict(zip(keys, values)) is the one-liner for 'two parallel lists into a mapping'. No loop, no index, no table[keys[i]] = values[i].",
    explanation_ru="dict(zip(keys, values)) – однострочник для «два параллельных списка в отображение». Без цикла, без индекса, без table[keys[i]] = values[i].",
)

VARIANTS = [
    dict(KEYS="['rope', 'lamp', 'map']", VALUES="[3, 12, 7]", TABLE="{'rope': 3, 'lamp': 12, 'map': 7}"),
    dict(KEYS="['BTC', 'ETH']", VALUES="[68000, 3500]", TABLE="{'BTC': 68000, 'ETH': 3500}"),
    dict(KEYS="['ann', 'bob']", VALUES="[1200, 1450]", TABLE="{'ann': 1200, 'bob': 1450}"),
]

STARTER = '''
keys = @KEYS@
values = @VALUES@
table = dict(___(keys, values))
# table == @TABLE@
'''

SOLUTION = '''
keys = @KEYS@
values = @VALUES@
table = dict(zip(keys, values))
'''

TESTS = '''
def test_table(ns, check):
    check(ns["table"], @TABLE@, "table")

def test_uses_zip(src, ast_tools, check):
    check(ast_tools.uses_name(src, "zip"), True, "zip is used")
'''
