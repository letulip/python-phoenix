META = dict(
    id="gym.dict-tools.group-by-key", type="rewrite", order=20,
    difficulty=1, minutes=1, world="bybit",
    concepts=["setdefault", "dict-basics"],
    title="Group with setdefault",
    statement_en="@NAME@(pairs) groups values by key with 'if key in groups ... else ...'. Rewrite the loop body as one line with setdefault: no if statement may remain.",
    hints_en=["groups.setdefault(key, []).append(value) creates the list on the first visit and appends every time."],
    hints_ru=["groups.setdefault(key, []).append(value) создаёт список при первом визите и добавляет каждый раз."],
    explanation_en="setdefault returns the existing list or stores and returns a new one, so 'create if missing, then append' collapses into one call. collections.defaultdict(list) is the next step when every key will be grouped.",
    explanation_ru="setdefault возвращает существующий список или сохраняет и возвращает новый, поэтому «создай, если нет, потом добавь» сворачивается в один вызов. collections.defaultdict(list) – следующий шаг, когда группируется каждый ключ.",
)

VARIANTS = [
    dict(NAME="by_symbol", SAMPLE="[('BTC', 1), ('ETH', 2), ('BTC', 3)]", EXPECT="{'BTC': [1, 3], 'ETH': [2]}"),
    dict(NAME="by_world", SAMPLE="[('game', 'Timmy'), ('tennis', 'Ada'), ('game', 'Byte')]", EXPECT="{'game': ['Timmy', 'Byte'], 'tennis': ['Ada']}"),
    dict(NAME="by_length", SAMPLE="[(3, 'map'), (4, 'rope'), (3, 'sun')]", EXPECT="{3: ['map', 'sun'], 4: ['rope']}"),
]

STARTER = '''
def @NAME@(pairs):
    groups = {}
    for key, value in pairs:
        if key in groups:
            groups[key].append(value)
        else:
            groups[key] = [value]
    return groups
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(pairs):
    groups = {}
    for key, value in pairs:
        groups.setdefault(key, []).append(value)
    return groups
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), {}, "@NAME@([])")

def test_setdefault(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "If"), 0, "no if statement left")
    check(ast_tools.count_calls(src, "setdefault") >= 1, True, "setdefault is used")
'''
