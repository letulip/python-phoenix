META = dict(
    id="gym.dict-tools.items-loop", type="rewrite", order=40,
    difficulty=1, minutes=1, world="everyday",
    concepts=["dict-basics"],
    title="Walk the pairs with items()",
    statement_en="@NAME@(@ARG@) loops over the keys and indexes the dict for every value. Rewrite the loop over @ARG@.items() with the pair unpacked in the for line: no indexing may remain.",
    hints_en=["for key, value in @ARG@.items(): gives both at once."],
    hints_ru=["for key, value in @ARG@.items(): даёт оба сразу."],
    explanation_en="Looping over a dict yields keys; items() yields the pairs, and unpacking them in the for line names both without a second lookup per iteration.",
    explanation_ru="Цикл по словарю выдаёт ключи; items() выдаёт пары, а распаковка в строке for называет обе части без второго поиска на каждой итерации.",
)

VARIANTS = [
    dict(NAME="price_lines", ARG="prices", SAMPLE="{'rope': 3, 'lamp': 12}", EXPECT="['rope: 3', 'lamp: 12']"),
    dict(NAME="score_lines", ARG="scores", SAMPLE="{'ann': 7, 'bob': 9}", EXPECT="['ann: 7', 'bob: 9']"),
    dict(NAME="stock_lines", ARG="stock", SAMPLE="{'potion': 3}", EXPECT="['potion: 3']"),
]

STARTER = '''
def @NAME@(@ARG@):
    lines = []
    for key in @ARG@:
        value = @ARG@[key]
        lines.append(f"{key}: {value}")
    return lines
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    lines = []
    for key, value in @ARG@.items():
        lines.append(f"{key}: {value}")
    return lines
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]({}), [], "@NAME@({})")

def test_items(src, ast_tools, check):
    check(ast_tools.count_calls(src, "items") >= 1, True, "items() is used")
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no indexing left")
'''
