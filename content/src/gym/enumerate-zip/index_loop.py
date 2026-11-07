META = dict(
    id="gym.enumerate-zip.index-loop", type="rewrite", order=10,
    difficulty=1, minutes=1, world="game",
    concepts=["enumerate", "range"],
    title="Numbers without range(len())",
    statement_en="@NAME@(@ARG@) numbers the items from 1 through range(len(...)) and indexing. Rewrite it with enumerate: no range() and no indexing may remain.",
    hints_en=["for number, item in enumerate(@ARG@, start=1): gives both the running number and the item."],
    hints_ru=["for number, item in enumerate(@ARG@, start=1): даёт и порядковый номер, и элемент."],
    explanation_en="enumerate hands out the position and the item together, and start=1 removes the i + 1 arithmetic. Nothing is indexed, so nothing can be off by one.",
    explanation_ru="enumerate выдаёт позицию и элемент вместе, а start=1 убирает арифметику i + 1. Ничего не индексируется, значит ничего не промахнётся на единицу.",
)

VARIANTS = [
    dict(NAME="numbered", ARG="names", SAMPLE="['ann', 'bob']", EXPECT="['1. ann', '2. bob']"),
    dict(NAME="agenda", ARG="topics", SAMPLE="['intro', 'demo', 'q&a']", EXPECT="['1. intro', '2. demo', '3. q&a']"),
    dict(NAME="ranking", ARG="players", SAMPLE="['Byte']", EXPECT="['1. Byte']"),
]

STARTER = '''
def @NAME@(@ARG@):
    lines = []
    for i in range(len(@ARG@)):
        lines.append(f"{i + 1}. {@ARG@[i]}")
    return lines
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    lines = []
    for number, item in enumerate(@ARG@, start=1):
        lines.append(f"{number}. {item}")
    return lines
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), [], "@NAME@([])")

def test_enumerate(src, ast_tools, check):
    check(ast_tools.uses_name(src, "enumerate"), True, "enumerate is used")
    check(ast_tools.count_calls(src, "range"), 0, "no range() left")
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no indexing left")
'''
