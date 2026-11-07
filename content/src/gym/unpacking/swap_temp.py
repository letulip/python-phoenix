META = dict(
    id="gym.unpacking.swap-temp", type="rewrite", order=20,
    difficulty=1, minutes=1, world="game",
    concepts=["tuple-unpacking"],
    title="Swap without a temp",
    statement_en="@NAME@(@A@, @B@) swaps two values through a temporary variable. Rewrite it with one tuple assignment: no temp variable may remain, and the function keeps returning the swapped pair.",
    hints_en=["@A@, @B@ = @B@, @A@ evaluates the right side first, then assigns both names."],
    hints_ru=["@A@, @B@ = @B@, @A@ сначала вычисляет правую часть, потом присваивает оба имени."],
    explanation_en="The right side of an assignment is built completely before anything is assigned, so a tuple swap needs no scratch variable. The same rule powers rotations like a, b, c = b, c, a.",
    explanation_ru="Правая часть присваивания строится целиком до того, как что-либо присвоено, поэтому обмену через кортеж не нужна временная переменная. То же правило даёт сдвиги вроде a, b, c = b, c, a.",
)

VARIANTS = [
    dict(NAME="swap", A="a", B="b", SAMPLE="1, 2", EXPECT="(2, 1)"),
    dict(NAME="switch_sides", A="left", B="right", SAMPLE="'Ada', 'Byte'", EXPECT="('Byte', 'Ada')"),
    dict(NAME="flip", A="x", B="y", SAMPLE="10, 20", EXPECT="(20, 10)"),
]

STARTER = '''
def @NAME@(@A@, @B@):
    temp = @A@
    @A@ = @B@
    @B@ = temp
    return @A@, @B@
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@A@, @B@):
    @A@, @B@ = @B@, @A@
    return @A@, @B@
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_same_values(ns, check):
    check(ns["@NAME@"](5, 5), (5, 5), "@NAME@(5, 5)")

def test_no_temp(src, ast_tools, check):
    check(ast_tools.uses_name(src, "temp"), False, "no temp variable left")
    check(ast_tools.body_lines(src) <= 3, True, "three lines at most")
'''
