META = dict(
    id="gym.comprehensions.transform-append", type="rewrite", order=20,
    difficulty=1, minutes=1, world="shorts",
    concepts=["list-comprehension", "str-methods"],
    title="Transform with a comprehension",
    statement_en="@NAME@(@ARG@) applies one string method to every item with a loop and append. Rewrite it as one list comprehension: no for statement may remain.",
    hints_en=["[w.@METHOD@() for w in @ARG@] is the whole return value."],
    hints_ru=["[w.@METHOD@() for w in @ARG@] – всё возвращаемое значение."],
    explanation_en="'A new list with f applied to every item' is exactly what a comprehension says. map(str.@METHOD@, @ARG@) says it too, and a senior knows both and picks the one the team reads faster.",
    explanation_ru="«Новый список, где f применена к каждому элементу» – ровно то, что говорит включение. map(str.@METHOD@, @ARG@) говорит то же, и сеньор знает оба варианта и выбирает тот, который команда читает быстрее.",
)

VARIANTS = [
    dict(NAME="shout", ARG="words", METHOD="upper", SAMPLE="['go', 'pixel']", EXPECT="['GO', 'PIXEL']"),
    dict(NAME="tidy", ARG="parts", METHOD="strip", SAMPLE="[' lake ', 'sunrise  ']", EXPECT="['lake', 'sunrise']"),
    dict(NAME="lower_all", ARG="tags", METHOD="lower", SAMPLE="['Lake', 'SUNRISE']", EXPECT="['lake', 'sunrise']"),
]

STARTER = '''
def @NAME@(@ARG@):
    result = []
    for w in @ARG@:
        result.append(w.@METHOD@())
    return result
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return [w.@METHOD@() for w in @ARG@]
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), [], "@NAME@([])")

def test_comprehension(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "For"), 0, "no for statement left")
    check(ast_tools.has_comprehension(src), True, "a comprehension is used")
'''
