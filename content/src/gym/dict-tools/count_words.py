META = dict(
    id="gym.dict-tools.count-words", type="rewrite", order=10,
    difficulty=1, minutes=1, world="shorts",
    concepts=["dict-get", "dict-basics"],
    title="Count without the key dance",
    statement_en="@NAME@(@ARG@) counts occurrences with 'if key in counts ... else ...'. Rewrite the loop body as one line with dict.get: no if statement may remain.",
    hints_en=["counts[item] = counts.get(item, 0) + 1 handles a new key and a known key alike."],
    hints_ru=["counts[item] = counts.get(item, 0) + 1 одинаково обрабатывает новый и уже известный ключ."],
    explanation_en="dict.get(key, 0) returns 0 for a missing key, so 'add one' is the same line in both cases. collections.Counter is the same idea with a name, and a senior mentions it right after writing this.",
    explanation_ru="dict.get(key, 0) возвращает 0 для отсутствующего ключа, поэтому «прибавь один» – одна и та же строка в обоих случаях. collections.Counter – та же идея с именем, и сеньор упоминает его сразу после этой строки.",
)

VARIANTS = [
    dict(NAME="count_words", ARG="words", SAMPLE="['a', 'b', 'a']", EXPECT="{'a': 2, 'b': 1}"),
    dict(NAME="tally", ARG="tags", SAMPLE="['#lake', '#lake', '#sun']", EXPECT="{'#lake': 2, '#sun': 1}"),
    dict(NAME="votes", ARG="choices", SAMPLE="['rope', 'map', 'rope', 'rope']", EXPECT="{'rope': 3, 'map': 1}"),
]

STARTER = '''
def @NAME@(@ARG@):
    counts = {}
    for item in @ARG@:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    counts = {}
    for item in @ARG@:
        counts[item] = counts.get(item, 0) + 1
    return counts
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), {}, "@NAME@([])")

def test_get(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "If"), 0, "no if statement left")
    check(ast_tools.count_calls(src, "get") >= 1, True, "dict.get is used")
'''
