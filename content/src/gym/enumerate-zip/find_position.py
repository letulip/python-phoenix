META = dict(
    id="gym.enumerate-zip.find-position", type="rewrite", order=50,
    difficulty=1, minutes=1, world="game",
    concepts=["enumerate", "for-loop"],
    title="Position without a hand counter",
    statement_en="@NAME@(@ARG@, target) keeps a counter that it bumps on every iteration. Rewrite it with enumerate so the position comes from the loop itself: no counter variable and no += may remain. Return -1 when the target is absent.",
    hints_en=["for position, item in enumerate(@ARG@): then return position on a match; return -1 after the loop."],
    hints_ru=["for position, item in enumerate(@ARG@): и верни position при совпадении; после цикла верни -1."],
    explanation_en="A counter bumped at the end of the loop body is enumerate written by hand, with one extra way to get it wrong (forgetting the bump on a continue). enumerate cannot drift.",
    explanation_ru="Счётчик, который увеличивают в конце тела цикла, – это enumerate, написанный руками, плюс лишний способ ошибиться (забыть увеличить при continue). enumerate не сбивается.",
)

VARIANTS = [
    dict(NAME="position_of", ARG="items", SAMPLE="['a', 'b', 'c'], 'b'", EXPECT="1"),
    dict(NAME="seat_of", ARG="names", SAMPLE="['ann', 'bob', 'cid'], 'cid'", EXPECT="2"),
    dict(NAME="slot_of", ARG="hotbar", SAMPLE="['sword', 'torch'], 'sword'", EXPECT="0"),
]

STARTER = '''
def @NAME@(@ARG@, target):
    position = 0
    for item in @ARG@:
        if item == target:
            return position
        position += 1
    return -1
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@, target):
    for position, item in enumerate(@ARG@):
        if item == target:
            return position
    return -1
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_missing_and_empty(ns, check):
    check((ns["@NAME@"](["a"], "z"), ns["@NAME@"]([], "a")), (-1, -1), "absent target, empty list")

def test_enumerate(src, ast_tools, check):
    check(ast_tools.uses_name(src, "enumerate"), True, "enumerate is used")
    check(ast_tools.count_nodes(src, "AugAssign"), 0, "no hand counter left")
'''
