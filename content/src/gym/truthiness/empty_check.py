META = dict(
    id="gym.truthiness.empty-check", type="rewrite", order=10,
    difficulty=1, minutes=1, world="game",
    concepts=["truthiness", "len"],
    title="Empty means falsy",
    statement_en="@NAME@(@ARG@) checks emptiness with len(...) == 0. Rewrite the check with truthiness: no len() call may remain.",
    hints_en=["An empty list, string or dict is falsy, so 'if not @ARG@:' is the whole check."],
    hints_ru=["Пустой список, строка или словарь ложны, поэтому if not @ARG@: – вся проверка."],
    explanation_en="'if not items' says 'if there is nothing here' and works for every container, while len(x) == 0 asks a number a question about emptiness. Reviewers read the first one without stopping.",
    explanation_ru="if not items говорит «если тут ничего нет» и работает для любого контейнера, а len(x) == 0 задаёт числу вопрос о пустоте. Первое ревьюер читает не останавливаясь.",
)

VARIANTS = [
    dict(NAME="status", ARG="items", EMPTY="empty", FULL="ready"),
    dict(NAME="cart_state", ARG="cart", EMPTY="nothing to pay", FULL="checkout"),
    dict(NAME="queue_state", ARG="queue", EMPTY="idle", FULL="busy"),
]

STARTER = '''
def @NAME@(@ARG@):
    if len(@ARG@) == 0:
        return "@EMPTY@"
    return "@FULL@"
'''

EXAMPLES = [
    {"call": "@NAME@([])", "expected": "'@EMPTY@'"},
    {"call": "@NAME@([1, 2])", "expected": "'@FULL@'"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    if not @ARG@:
        return "@EMPTY@"
    return "@FULL@"
'''

TESTS = '''
def test_empty_and_full(ns, check):
    check((ns["@NAME@"]([]), ns["@NAME@"]([1, 2])), ("@EMPTY@", "@FULL@"), "empty list, two items")

def test_other_containers(ns, check):
    check((ns["@NAME@"](""), ns["@NAME@"]({}), ns["@NAME@"]("x")), ("@EMPTY@", "@EMPTY@", "@FULL@"), "empty str, empty dict, 'x'")

def test_truthiness(src, ast_tools, check):
    check(ast_tools.count_calls(src, "len"), 0, "no len() left")
    check(ast_tools.count_nodes(src, "Not") >= 1, True, "uses 'not'")
'''
