META = dict(
    id="gym.guards.flag-loop-all", type="rewrite", order=30,
    difficulty=1, minutes=1, world="tennis",
    concepts=["any-all", "for-loop"],
    title="A flag loop is all()",
    statement_en="@NAME@(@ARG@) starts with True and flips to False when one value fails. Rewrite it as one return with all() over a generator: no for statement and no flag may remain.",
    hints_en=["return all(x @OP@ @LIMIT@ for x in @ARG@); all of nothing is True."],
    hints_ru=["return all(x @OP@ @LIMIT@ for x in @ARG@); «все» из ничего – True."],
    explanation_en="'Do they all pass?' is all(). It stops at the first failure, and for an empty input it returns True, the vacuous truth, which is exactly what the flag loop returned too.",
    explanation_ru="«Все ли проходят?» – это all(). Останавливается на первом провале, а для пустого входа возвращает True, пустую истину, ровно то же, что возвращал и цикл с флагом.",
)

VARIANTS = [
    dict(NAME="all_in", ARG="serves", OP="<=", LIMIT="200", SAMPLE="[180, 195, 172]", EXPECT="True"),
    dict(NAME="all_positive", ARG="balances", OP=">", LIMIT="0", SAMPLE="[50, -5, 20]", EXPECT="False"),
    dict(NAME="all_passed", ARG="scores", OP=">=", LIMIT="50", SAMPLE="[61, 75, 90]", EXPECT="True"),
]

STARTER = '''
def @NAME@(@ARG@):
    ok = True
    for x in @ARG@:
        if not (x @OP@ @LIMIT@):
            ok = False
    return ok
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return all(x @OP@ @LIMIT@ for x in @ARG@)
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), True, "@NAME@([]) is True: nothing fails")

def test_all(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statement left")
    check(ast_tools.uses_name(src, "all"), True, "all is used")
'''
