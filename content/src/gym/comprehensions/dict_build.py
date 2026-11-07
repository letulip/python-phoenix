META = dict(
    id="gym.comprehensions.dict-build", type="rewrite", order=30,
    difficulty=2, minutes=1, world="tennis",
    concepts=["dict-comprehension"],
    title="Build a dict with a comprehension",
    statement_en="@NAME@(pairs) builds a dict from (key, value) pairs, computing each stored value, with a loop. Rewrite it as one dict comprehension: no for statement may remain.",
    hints_en=["{key: @EXPR@ for key, value in pairs} is the whole return value."],
    hints_ru=["{key: @EXPR@ for key, value in pairs} – всё возвращаемое значение."],
    explanation_en="A dict comprehension earns its place when the key or the value is computed; when they are stored as they come, dict(pairs) is even shorter. Here the value changes, so the comprehension is the right tool.",
    explanation_ru="Включение словаря оправдано, когда ключ или значение вычисляются; если они кладутся как есть, dict(pairs) ещё короче. Здесь значение меняется, так что включение – верный инструмент.",
)

VARIANTS = [
    dict(NAME="doubled", EXPR="value * 2", SAMPLE="[('ann', 10), ('bob', 7)]", EXPECT="{'ann': 20, 'bob': 14}"),
    dict(NAME="rounded", EXPR="round(value)", SAMPLE="[('ann', 10.4), ('bob', 7.6)]", EXPECT="{'ann': 10, 'bob': 8}"),
    dict(NAME="as_percent", EXPR="value * 100", SAMPLE="[('serve', 0.65), ('return', 0.4)]", EXPECT="{'serve': 65.0, 'return': 40.0}"),
]

STARTER = '''
def @NAME@(pairs):
    table = {}
    for key, value in pairs:
        table[key] = @EXPR@
    return table
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(pairs):
    return {key: @EXPR@ for key, value in pairs}
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), {}, "@NAME@([])")

def test_dict_comprehension(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statement left")
    check(ast_tools.count_nodes(src, "DictComp") >= 1, True, "a dict comprehension is used")
'''
