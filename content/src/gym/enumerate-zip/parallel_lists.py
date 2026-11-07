META = dict(
    id="gym.enumerate-zip.parallel-lists", type="rewrite", order=20,
    difficulty=1, minutes=2, world="everyday",
    concepts=["zip", "sum", "range"],
    title="Two lists side by side",
    statement_en="@NAME@(@A@, @B@) multiplies two lists position by position through a shared index. Rewrite it with zip: no range() and no indexing may remain.",
    hints_en=["zip(@A@, @B@) yields pairs; sum(x * y for x, y in zip(@A@, @B@)) is the whole body."],
    hints_ru=["zip(@A@, @B@) выдаёт пары; sum(x * y for x, y in zip(@A@, @B@)) – всё тело функции."],
    explanation_en="zip pairs the lists by position and stops at the shorter one, so the loop reads 'for each pair' instead of 'for each index'. With sum over a generator the accumulator disappears too.",
    explanation_ru="zip соединяет списки по позициям и останавливается на более коротком, поэтому цикл читается «для каждой пары», а не «для каждого индекса». С sum по генератору исчезает и накопитель.",
)

VARIANTS = [
    dict(NAME="order_total", A="quantities", B="prices", SAMPLE="[1, 2, 3], [4, 5, 6]", EXPECT="32"),
    dict(NAME="dot", A="xs", B="ys", SAMPLE="[2, 3], [10, 10]", EXPECT="50"),
    dict(NAME="bill", A="hours", B="rates", SAMPLE="[8, 2], [10, 25]", EXPECT="130"),
]

STARTER = '''
def @NAME@(@A@, @B@):
    total = 0
    for i in range(len(@A@)):
        total += @A@[i] * @B@[i]
    return total
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@A@, @B@):
    return sum(x * y for x, y in zip(@A@, @B@))
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([], []), 0, "@NAME@([], [])")

def test_zip(src, ast_tools, check):
    check(ast_tools.uses_name(src, "zip"), True, "zip is used")
    check(ast_tools.count_calls(src, "range"), 0, "no range() left")
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no indexing left")
'''
