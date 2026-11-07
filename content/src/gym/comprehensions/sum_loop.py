META = dict(
    id="gym.comprehensions.sum-loop", type="rewrite", order=40,
    difficulty=1, minutes=1, world="shorts",
    concepts=["sum", "comprehension-if"],
    title="sum over a generator",
    statement_en="@NAME@(@ARG@) adds up one field of every record with an accumulator loop. Rewrite it as sum over a generator expression: no for statement and no accumulator may remain.",
    hints_en=["sum(item['@KEY@'] for item in @ARG@) is the whole return value; sum of nothing is 0."],
    hints_ru=["sum(item['@KEY@'] for item in @ARG@) – всё возвращаемое значение; сумма пустоты – 0."],
    explanation_en="total = 0 plus += in a loop is sum() spelled by hand. The generator feeds sum one value at a time, so no intermediate list is built either.",
    explanation_ru="total = 0 плюс += в цикле – это sum(), написанный руками. Генератор отдаёт sum по одному значению, так что промежуточный список тоже не строится.",
)

VARIANTS = [
    dict(NAME="total_views", ARG="videos", KEY="views", SAMPLE="[{'views': 900}, {'views': 1200}]", EXPECT="2100"),
    dict(NAME="total_games", ARG="matches", KEY="games", SAMPLE="[{'games': 12}, {'games': 18}, {'games': 9}]", EXPECT="39"),
    dict(NAME="total_qty", ARG="orders", KEY="qty", SAMPLE="[{'qty': 2.5}, {'qty': 1.5}]", EXPECT="4.0"),
]

STARTER = '''
def @NAME@(@ARG@):
    total = 0
    for item in @ARG@:
        total += item["@KEY@"]
    return total
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return sum(item["@KEY@"] for item in @ARG@)
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), 0, "@NAME@([])")

def test_sum(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statement left")
    check(ast_tools.uses_name(src, "sum"), True, "sum is used")
    check(ast_tools.count_nodes(src, "AugAssign"), 0, "no accumulator left")
'''
