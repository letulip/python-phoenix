META = dict(
    id="l0.collections.merge-stock", type="task", order=62,
    difficulty=1, minutes=5, world="game",
    concepts=["dict-basics", "dict-get"],
    story_en="Timmy found a second chest. Now he has two chests with sticks in both, and a strong wish to see one number.",
    title="Merge two chests",
    statement_en=("Write merge_stock(a, b) -> dict. Both are dicts of item -> count. Return a new dict that holds every "
                  "item from either chest with the counts added up. Neither input may be modified. Keep the items of a "
                  "first, in their order, then the items that exist only in b."),
    hints_en=[
        "Start from a copy of a: dict(a) or a.copy(), never from a itself.",
        "For each item in b, add its count to what the copy already has: merged.get(item, 0) + count.",
        "Return the copy; nothing else needs to change.",
    ],
    hints_ru=[
        "Начни с копии a: dict(a) или a.copy(), но не с самого a.",
        "Для каждого предмета из b прибавь его количество к тому, что уже есть в копии: merged.get(item, 0) + count.",
        "Верни копию; больше ничего менять не нужно.",
    ],
    explanation_en=("Copy, then add: a new dict keeps the inputs intact, and dict.get with a default of 0 makes 'present in "
                    "one chest only' and 'present in both' the same line of code. Key order follows insertion, so a's "
                    "items come first automatically."),
    explanation_ru=("Скопируй, потом прибавляй: новый словарь оставляет входы целыми, а dict.get с умолчанием 0 делает "
                    "«есть только в одном сундуке» и «есть в обоих» одной строкой кода. Порядок ключей – порядок вставки, "
                    "поэтому предметы из a сами идут первыми."),
    talk_track=[
        "Say you copy a first so the inputs stay untouched.",
        "Mention dict.get(item, 0) merges the two cases into one line.",
        "Complexity O(n + m) in the sizes of the chests.",
    ],
    complexity="O(n + m)",
    followups=["How would collections.Counter change this?", "What if counts can be negative, like an IOU?"],
)

STARTER = '''
def merge_stock(a, b):
    ...
'''

EXAMPLES = [
    {"call": "merge_stock({'stick': 2}, {'stick': 1, 'coal': 3})", "expected": "{'stick': 3, 'coal': 3}"},
    {"call": "merge_stock({}, {'gem': 1})", "expected": "{'gem': 1}"},
]

SOLUTION = '''
def merge_stock(a, b):
    merged = dict(a)
    for item, count in b.items():
        merged[item] = merged.get(item, 0) + count
    return merged
'''

TESTS = '''
def test_overlap(ns, check):
    check(ns["merge_stock"]({"stick": 2}, {"stick": 1, "coal": 3}), {"stick": 3, "coal": 3}, "sticks add up, coal joins")

def test_disjoint(ns, check):
    check(ns["merge_stock"]({"rope": 1}, {"gem": 1}), {"rope": 1, "gem": 1}, "disjoint chests")

def test_empty(ns, check):
    check((ns["merge_stock"]({}, {}), ns["merge_stock"]({}, {"gem": 1})), ({}, {"gem": 1}), "empty chests")

def test_inputs_untouched(ns, check):
    a, b = {"stick": 2}, {"stick": 1}
    out = ns["merge_stock"](a, b)
    check((a, b), ({"stick": 2}, {"stick": 1}), "inputs unchanged")
    check(out is a, False, "a new dict is returned")

def test_key_order(ns, check):
    check(list(ns["merge_stock"]({"b": 1, "a": 1}, {"c": 1, "a": 1})), ["b", "a", "c"], "a's keys first, then b's new ones")
'''

LEVELS = dict(
    middle=dict(
        code='''
def merge_stock(a, b):
    result = {}
    for item in a:
        result[item] = a[item]
    for item in b:
        if item in result:
            result[item] = result[item] + b[item]
        else:
            result[item] = b[item]
    return result
''',
        note_en=("Correct, and it respects the inputs. The first loop is dict(a) spelled by hand, and the if/else is the "
                 "'key present or not' dance that dict.get was invented to replace. A reviewer reads it fine; a reviewer "
                 "also sees that you did not reach for the built-in tools."),
        note_ru=("Верно, и входы не тронуты. Но первый цикл – это dict(a), написанный вручную, а if/else – тот самый танец "
                 "«ключ есть или нет», ради которого придумали dict.get. Ревьюер читает без труда; ревьюер также видит, "
                 "что ты не взял встроенные инструменты."),
    ),
    senior=dict(
        code='''
def merge_stock(a, b):
    """New dict with the counts of both chests added up; the inputs stay untouched."""
    merged = dict(a)
    for item, count in b.items():
        merged[item] = merged.get(item, 0) + count
    return merged
''',
        note_en=("Copy once, then one line per item with .get(item, 0): the two cases collapse. A senior also knows that "
                 "collections.Counter(a) + Counter(b) is the one-liner, and explains why it is not used here: it drops "
                 "zero and negative counts and returns a Counter, not the plain dict the caller asked for. Knowing the "
                 "tool and its edge cases beats using it blindly."),
        note_ru=("Одна копия, потом одна строка на предмет через .get(item, 0): два случая схлопнулись. Сеньор также знает, "
                 "что collections.Counter(a) + Counter(b) – однострочник, и объясняет, почему здесь он не взят: тот "
                 "выбрасывает нулевые и отрицательные количества и возвращает Counter, а не обычный dict, который просили. "
                 "Знать инструмент вместе с его краями важнее, чем применить его вслепую."),
    ),
)
