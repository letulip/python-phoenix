META = dict(
    id="l0.comprehensions.loop-to-comprehension", type="refactor", order=80,
    difficulty=2, minutes=6, world="tennis",
    concepts=["list-comprehension", "dict-comprehension", "comprehension-if"],
    story_en="The sorting machine's manual, written by the previous engineer, builds every list with four lines. Pixel has opinions.",
    title="Loop to comprehension",
    statement_en=("Both functions work but build a list and a dict with four-line loops. Rewrite each body as a single "
                  "comprehension so that no for statement is left in the file. Behaviour must not change."),
    hints_en=[
        "A filtering loop with append becomes [x for x in items if condition].",
        "A dict-building loop becomes {key: value for key, value in pairs}.",
        "Return the comprehension directly; no temporary list or dict is needed.",
    ],
    hints_ru=[
        "Фильтрующий цикл с append становится [x for x in items if condition].",
        "Цикл, собирающий словарь, становится {key: value for key, value in pairs}.",
        "Возвращай включение напрямую; временный список или словарь не нужен.",
    ],
    explanation_en=("A comprehension states what the result is instead of how to build it, and removes the temporary "
                    "variable and the append call. For pairs, dict(players) is an even shorter spelling."),
    explanation_ru=("Включение описывает, что получится, а не как это собрать, и убирает временную переменную и вызов append. "
                    "Для пар ещё короче пишется dict(players)."),
    talk_track=[
        "Say a comprehension states what the result is, not how to build it.",
        "Mention the dict comprehension, and that dict(players) also works for pairs.",
    ],
    complexity="O(n) each",
    followups=["When would you keep the loop instead?", "How should rating_by_name treat duplicate names?"],
)

STARTER = '''
def long_rallies(rallies):
    result = []
    for r in rallies:
        if r >= 10:
            result.append(r)
    return result

def rating_by_name(players):
    table = {}
    for name, rating in players:
        table[name] = rating
    return table
'''

EXAMPLES = [
    {"call": "long_rallies([12, 3, 10, 9])", "expected": "[12, 10]"},
    {"call": "rating_by_name([('Ada', 1200), ('Byte', 1450)])", "expected": "{'Ada': 1200, 'Byte': 1450}"},
]

SOLUTION = '''
def long_rallies(rallies):
    return [r for r in rallies if r >= 10]

def rating_by_name(players):
    return {name: rating for name, rating in players}
'''

SOLUTION_ALT = '''
def long_rallies(rallies):
    return [r for r in rallies if r >= 10]

def rating_by_name(players):
    return dict(players)
'''

TESTS = '''
def test_long_rallies(ns, check):
    check(ns["long_rallies"]([12, 3, 10, 9]), [12, 10], "long_rallies([12, 3, 10, 9])")

def test_long_rallies_empty(ns, check):
    check(ns["long_rallies"]([]), [], "long_rallies([])")

def test_rating_by_name(ns, check):
    check(ns["rating_by_name"]([("Ada", 1200), ("Byte", 1450)]), {"Ada": 1200, "Byte": 1450}, "rating_by_name")

def test_rating_by_name_empty(ns, check):
    check(ns["rating_by_name"]([]), {}, "rating_by_name([])")

def test_no_for_statements(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statements left")

def test_uses_comprehension(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "ListComp") >= 1, True, "a list comprehension is used")
'''
