META = dict(
    id="gym.slices.all-but-last", type="rewrite", order=12,
    difficulty=1, minutes=1, world="neutral",
    concepts=["slicing", "list-index"],
    title="Everything but the last",
    statement_en="@NAME@(@ARG@) copies every item except the last one with an index loop. Rewrite it as a single slice: no loop and no range() may remain.",
    hints_en=["A negative stop counts from the end: @ARG@[:-1] is everything before the last item, and it is already a new list."],
    hints_ru=["Отрицательный stop считает с конца: @ARG@[:-1] – всё до последнего элемента, и это уже новый список."],
    explanation_en="A slice is a copy of a range of positions in one expression. range(len(x) - 1) with x[i] rebuilds the same copy by hand, with an off-by-one waiting to happen.",
    explanation_ru="Срез – копия диапазона позиций одним выражением. range(len(x) - 1) с x[i] собирает ту же копию руками, и ошибка на единицу уже ждёт своего часа.",
)

VARIANTS = [
    dict(NAME="drop_last", ARG="items", SAMPLE="[1, 2, 3]", EXPECT="[1, 2]"),
    dict(NAME="without_newest", ARG="prices", SAMPLE="[5, 6, 7, 8]", EXPECT="[5, 6, 7]"),
    dict(NAME="all_but_last", ARG="names", SAMPLE="['ann', 'bob']", EXPECT="['ann']"),
]

STARTER = '''
def @NAME@(@ARG@):
    result = []
    for i in range(len(@ARG@) - 1):
        result.append(@ARG@[i])
    return result
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return @ARG@[:-1]
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_short_lists(ns, check):
    check((ns["@NAME@"]([]), ns["@NAME@"]([9])), ([], []), "empty and one-item lists")

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
