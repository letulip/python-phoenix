META = dict(
    id="gym.join.csv-line", type="rewrite", order=10,
    difficulty=1, minutes=1, world="bybit",
    concepts=["split-join", "for-loop"],
    title="Comma line without the trailing cut",
    statement_en="@NAME@(@ARG@) glues the values with commas and then chops the last comma off. Rewrite it with ','.join over the string forms of the values: no += and no slicing may remain.",
    hints_en=["','.join(str(value) for value in @ARG@) puts commas only between the values."],
    hints_ru=["','.join(str(value) for value in @ARG@) ставит запятые только между значениями."],
    explanation_en="The trailing separator plus [:-1] is the signature of a hand-built string. join never produces one, works for an empty list, and reads as what it does.",
    explanation_ru="Хвостовой разделитель плюс [:-1] – подпись строки, собранной руками. join такого никогда не производит, работает для пустого списка и читается как то, что делает.",
)

VARIANTS = [
    dict(NAME="csv_line", ARG="values", SAMPLE="[1, 2, 3]", EXPECT="'1,2,3'"),
    dict(NAME="tag_line", ARG="tags", SAMPLE="['lake', 'sunrise']", EXPECT="'lake,sunrise'"),
    dict(NAME="ids_line", ARG="ids", SAMPLE="[42, 7, 19]", EXPECT="'42,7,19'"),
]

STARTER = '''
def @NAME@(@ARG@):
    line = ""
    for value in @ARG@:
        line += str(value) + ","
    return line[:-1]
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return ",".join(str(value) for value in @ARG@)
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_single_and_empty(ns, check):
    check((ns["@NAME@"]([5]), ns["@NAME@"]([])), ("5", ""), "one value and no values")

def test_join_used(src, ast_tools, check):
    check(ast_tools.count_calls(src, "join") >= 1, True, "join is used")
    check(ast_tools.count_nodes(src, "AugAssign"), 0, "no += left")
    check(ast_tools.count_nodes(src, "Slice"), 0, "no [:-1] trimming left")
'''
