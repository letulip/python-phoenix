META = dict(
    id="gym.slices.last-item", type="rewrite", order=10,
    difficulty=1, minutes=1, world="neutral",
    concepts=["list-index", "slicing"],
    title="The last item",
    statement_en="last(items) works, but it computes the index of the last element by hand. Rewrite it with a negative index: no len() call may remain.",
    hints_en=["Negative indexes count from the end: items[-1] is the last element, items[-2] the one before it."],
    hints_ru=["Отрицательные индексы считают с конца: items[-1] – последний элемент, items[-2] – предпоследний."],
    explanation_en="items[-1] is the idiom for 'the last one'. len(items) - 1 says the same with arithmetic the reader has to check.",
    explanation_ru="items[-1] – идиома для «последний». len(items) - 1 говорит то же самое арифметикой, которую читателю приходится проверять.",
)

VARIANTS = [
    dict(NAME="last", ARG="items", CALL="last(['rope', 'lamp', 'map'])", EXPECT="'map'", SAMPLE="['rope', 'lamp', 'map']", SAMPLE_LAST="'map'"),
    dict(NAME="newest", ARG="prices", CALL="newest([68000, 67950, 68210])", EXPECT="68210", SAMPLE="[68000, 67950, 68210]", SAMPLE_LAST="68210"),
    dict(NAME="final_word", ARG="words", CALL="final_word('no lemon no melon'.split())", EXPECT="'melon'", SAMPLE="['game', 'set', 'match']", SAMPLE_LAST="'match'"),
]

STARTER = '''
def @NAME@(@ARG@):
    return @ARG@[len(@ARG@) - 1]
'''

EXAMPLES = [
    {"call": "@CALL@", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return @ARG@[-1]
'''

TESTS = '''
def test_last(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @SAMPLE_LAST@, "@NAME@(@SAMPLE@)")

def test_single(ns, check):
    check(ns["@NAME@"]([7]), 7, "a one-item list")

def test_no_len(src, ast_tools, check):
    check(ast_tools.count_calls(src, "len"), 0, "no len() call left")
'''
