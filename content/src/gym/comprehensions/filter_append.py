META = dict(
    id="gym.comprehensions.filter-append", type="rewrite", order=10,
    difficulty=1, minutes=1, world="tennis",
    concepts=["list-comprehension", "comprehension-if"],
    title="Filter with a comprehension",
    statement_en="@NAME@(@ARG@) keeps the values that pass a test, with a loop and append. Rewrite it as one list comprehension: no for statement may remain.",
    hints_en=["[x for x in @ARG@ if x @OP@ @LIMIT@] is the whole return value."],
    hints_ru=["[x for x in @ARG@ if x @OP@ @LIMIT@] – всё возвращаемое значение."],
    explanation_en="The comprehension names the result, 'the items that pass', instead of the steps that build it. No temporary list, no append, nothing to initialise before the loop.",
    explanation_ru="Включение называет результат, «элементы, которые проходят», а не шаги, которые его строят. Ни временного списка, ни append, ничего не нужно создавать до цикла.",
)

VARIANTS = [
    dict(NAME="long_rallies", ARG="rallies", OP=">=", LIMIT="10", SAMPLE="[12, 3, 10, 9]", EXPECT="[12, 10]"),
    dict(NAME="cheap", ARG="prices", OP="<", LIMIT="5", SAMPLE="[3, 12, 4, 7]", EXPECT="[3, 4]"),
    dict(NAME="passed", ARG="scores", OP=">=", LIMIT="50", SAMPLE="[61, 48, 75, 33]", EXPECT="[61, 75]"),
]

STARTER = '''
def @NAME@(@ARG@):
    result = []
    for x in @ARG@:
        if x @OP@ @LIMIT@:
            result.append(x)
    return result
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return [x for x in @ARG@ if x @OP@ @LIMIT@]
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), [], "@NAME@([])")

def test_comprehension(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statement left")
    check(ast_tools.count_nodes(src, "ListComp") >= 1, True, "a list comprehension is used")
'''
