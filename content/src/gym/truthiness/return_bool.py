META = dict(
    id="gym.truthiness.return-bool", type="rewrite", order=30,
    difficulty=1, minutes=1, world="tennis",
    concepts=["truthiness", "ternary"],
    title="Return the condition",
    statement_en="@NAME@ answers True or False through an if/else. Rewrite it as a single return of the comparison itself: no if statement may remain.",
    hints_en=["A comparison already is a bool: return @A@ @OP@ @B@."],
    hints_ru=["Сравнение уже и есть bool: return @A@ @OP@ @B@."],
    explanation_en="'if cond: return True else: return False' is four lines that say 'return cond'. The same applies to assignments: flag = cond, not an if/else.",
    explanation_ru="if cond: return True else: return False – четыре строки, которые говорят return cond. То же с присваиванием: flag = cond, а не if/else.",
)

VARIANTS = [
    dict(NAME="is_adult", A="age", B="limit", OP=">=", T_ARGS="30, 18", F_ARGS="10, 18"),
    dict(NAME="can_afford", A="balance", B="price", OP=">=", T_ARGS="50, 20", F_ARGS="5, 20"),
    dict(NAME="is_longer", A="rally", B="record", OP=">", T_ARGS="12, 9", F_ARGS="9, 9"),
]

STARTER = '''
def @NAME@(@A@, @B@):
    if @A@ @OP@ @B@:
        return True
    else:
        return False
'''

EXAMPLES = [
    {"call": "@NAME@(@T_ARGS@)", "expected": "True"},
    {"call": "@NAME@(@F_ARGS@)", "expected": "False"},
]

SOLUTION = '''
def @NAME@(@A@, @B@):
    return @A@ @OP@ @B@
'''

TESTS = '''
def test_both_cases(ns, check):
    check((ns["@NAME@"](@T_ARGS@), ns["@NAME@"](@F_ARGS@)), (True, False), "a true case and a false case")

def test_returns_bool(ns, check):
    check(type(ns["@NAME@"](@T_ARGS@)), bool, "the result is a bool")

def test_no_if(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "If") + ast_tools.count_nodes(src, "IfExp"), 0, "no if left, the comparison is returned")
'''
