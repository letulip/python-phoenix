META = dict(
    id="gym.guards.flag-loop-any", type="rewrite", order=20,
    difficulty=1, minutes=1, world="bybit",
    concepts=["any-all", "for-loop"],
    title="A flag loop is any()",
    statement_en="@NAME@(@ARG@) sets a flag inside a loop as soon as one value passes. Rewrite it as one return with any() over a generator: no for statement and no flag may remain.",
    hints_en=["return any(x @OP@ @LIMIT@ for x in @ARG@); any stops at the first hit."],
    hints_ru=["return any(x @OP@ @LIMIT@ for x in @ARG@); any останавливается на первом попадании."],
    explanation_en="'Is there at least one?' is any(). It reads as the question, stops early like a break would, and gives False for an empty input without a special case.",
    explanation_ru="«Есть ли хотя бы один?» – это any(). Читается как вопрос, останавливается рано, как break, и даёт False для пустого входа без особого случая.",
)

VARIANTS = [
    dict(NAME="has_spike", ARG="prices", OP=">", LIMIT="70000", SAMPLE="[64000, 71000, 68000]", EXPECT="True"),
    dict(NAME="has_fault", ARG="speeds", OP="<", LIMIT="150", SAMPLE="[180, 195, 172]", EXPECT="False"),
    dict(NAME="any_failed", ARG="scores", OP="<", LIMIT="50", SAMPLE="[61, 48, 75]", EXPECT="True"),
]

STARTER = '''
def @NAME@(@ARG@):
    found = False
    for x in @ARG@:
        if x @OP@ @LIMIT@:
            found = True
    return found
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return any(x @OP@ @LIMIT@ for x in @ARG@)
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), False, "@NAME@([])")

def test_any(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statement left")
    check(ast_tools.uses_name(src, "any"), True, "any is used")
'''
