META = dict(
    id="gym.slices.reverse-copy", type="rewrite", order=14,
    difficulty=1, minutes=1, world="neutral",
    concepts=["slicing", "list-index"],
    title="Backwards copy",
    statement_en="@NAME@(@ARG@) builds the reversed list with a counting-down range. Rewrite it as one slice with a negative step: no loop and no range() may remain, and the input must stay untouched.",
    hints_en=["@ARG@[::-1] walks the whole list with step -1 and returns a new list."],
    hints_ru=["@ARG@[::-1] проходит весь список с шагом -1 и возвращает новый список."],
    explanation_en="[::-1] is the reversed copy in one expression. reversed(x) is its lazy twin for a loop; x.reverse() flips the original in place and returns None, which is the one to avoid when the input must not change.",
    explanation_ru="[::-1] – перевёрнутая копия одним выражением. reversed(x) – её ленивый близнец для цикла; x.reverse() переворачивает оригинал на месте и возвращает None, и именно его избегают, когда вход менять нельзя.",
)

VARIANTS = [
    dict(NAME="backwards", ARG="steps", SAMPLE="[1, 2, 3]", EXPECT="[3, 2, 1]"),
    dict(NAME="reversed_names", ARG="names", SAMPLE="['ann', 'bob', 'cid']", EXPECT="['cid', 'bob', 'ann']"),
    dict(NAME="countdown", ARG="numbers", SAMPLE="[10, 20, 30, 40]", EXPECT="[40, 30, 20, 10]"),
]

STARTER = '''
def @NAME@(@ARG@):
    result = []
    for i in range(len(@ARG@) - 1, -1, -1):
        result.append(@ARG@[i])
    return result
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return @ARG@[::-1]
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), [], "@NAME@([])")

def test_input_untouched(ns, check):
    data = [1, 2, 3]
    out = ns["@NAME@"](data)
    check(data, [1, 2, 3], "input unchanged")
    check(out is data, False, "a new list comes back")

def test_slice_not_loop(src, ast_tools, check):
    check(ast_tools.has_loop(src), False, "no loop left")
    check(ast_tools.count_calls(src, "range"), 0, "no range() left")
    check(ast_tools.count_nodes(src, "Slice") >= 1, True, "a slice is used")
'''
