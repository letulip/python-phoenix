META = dict(
    id="gym.guards.if-else-assign", type="rewrite", order=40,
    difficulty=1, minutes=1, world="everyday",
    concepts=["ternary"],
    title="One value, two branches",
    statement_en="@NAME@(@ARG@) picks one of two strings through an if/else that assigns a variable. Rewrite it as a single return with a conditional expression: no if statement may remain.",
    hints_en=['return "@A@" if @COND@ else "@B@" is the whole body.'],
    hints_ru=['return "@A@" if @COND@ else "@B@" – всё тело функции.'],
    explanation_en="A conditional expression is for choosing a value, not for doing two different things. When both branches only assign the same name, it is the honest form; when they do more, keep the if.",
    explanation_ru="Условное выражение – для выбора значения, а не для двух разных действий. Когда обе ветки лишь присваивают одно имя, это честная форма; когда делают больше, оставь if.",
)

VARIANTS = [
    dict(NAME="size_label", ARG="n", COND="n > 10", A="big", B="small", T="20", F="3"),
    dict(NAME="parity", ARG="n", COND="n % 2 == 0", A="even", B="odd", T="8", F="7"),
    dict(NAME="heat", ARG="temp", COND="temp >= 25", A="hot", B="mild", T="31", F="18"),
]

STARTER = '''
def @NAME@(@ARG@):
    if @COND@:
        label = "@A@"
    else:
        label = "@B@"
    return label
'''

EXAMPLES = [
    {"call": "@NAME@(@T@)", "expected": "'@A@'"},
    {"call": "@NAME@(@F@)", "expected": "'@B@'"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return "@A@" if @COND@ else "@B@"
'''

TESTS = '''
def test_both_branches(ns, check):
    check((ns["@NAME@"](@T@), ns["@NAME@"](@F@)), ("@A@", "@B@"), "both branches")

def test_conditional_expression(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "If"), 0, "no if statement left")
    check(ast_tools.count_nodes(src, "IfExp") >= 1, True, "a conditional expression is used")
'''
