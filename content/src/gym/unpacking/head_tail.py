META = dict(
    id="gym.unpacking.head-tail", type="rewrite", order=30,
    difficulty=1, minutes=1, world="game",
    concepts=["tuple-unpacking", "star-args", "list-index"],
    title="Head and tail with a star",
    statement_en="@NAME@(@ARG@) takes the first item with [0] and the rest with [1:]. Rewrite it with star unpacking in one line: no indexing and no slicing may remain.",
    hints_en=["first, *rest = @ARG@ puts the first item in first and everything else, as a list, in rest."],
    hints_ru=["first, *rest = @ARG@ кладёт первый элемент в first, а всё остальное, списком, в rest."],
    explanation_en="The starred name absorbs 'whatever is left', so head/tail splits need neither index nor slice. It also works at the end (*init, last = items) and in the middle.",
    explanation_ru="Имя со звёздочкой вбирает «всё, что осталось», поэтому разделению на голову и хвост не нужны ни индекс, ни срез. Работает и в конце (*init, last = items), и в середине.",
)

VARIANTS = [
    dict(NAME="split_head", ARG="items", SAMPLE="[1, 2, 3]", EXPECT="(1, [2, 3])"),
    dict(NAME="leader_and_pack", ARG="runners", SAMPLE="['ann', 'bob', 'cid']", EXPECT="('ann', ['bob', 'cid'])"),
    dict(NAME="captain_and_crew", ARG="crew", SAMPLE="['Byte', 'Pixel']", EXPECT="('Byte', ['Pixel'])"),
]

STARTER = '''
def @NAME@(@ARG@):
    first = @ARG@[0]
    rest = @ARG@[1:]
    return first, rest
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    first, *rest = @ARG@
    return first, rest
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_single(ns, check):
    check(ns["@NAME@"]([7]), (7, []), "a one-item list leaves an empty rest")

def test_star(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no indexing or slicing left")
    check(ast_tools.count_nodes(src, "Starred") >= 1, True, "star unpacking is used")
'''
