META = dict(
    id="gym.unpacking.index-fields", type="rewrite", order=10,
    difficulty=1, minutes=1, world="tennis",
    concepts=["tuple-unpacking", "list-index"],
    title="Name the fields",
    statement_en="@NAME@(@ARG@) reads the two fields of a pair through [0] and [1]. Rewrite it with tuple unpacking so both parts get names in one line: no indexing may remain.",
    hints_en=["@A@, @B@ = @ARG@ replaces both index lines."],
    hints_ru=["@A@, @B@ = @ARG@ заменяет обе строки с индексами."],
    explanation_en="Unpacking names the parts where they enter the function; the reader never translates positions in their head, and a pair with the wrong number of fields fails loudly instead of silently reading the wrong slot.",
    explanation_ru="Распаковка называет части там, где они входят в функцию; читателю не нужно переводить позиции в уме, а пара с неверным числом полей падает громко вместо того, чтобы тихо прочитать не тот слот.",
)

VARIANTS = [
    dict(NAME="describe", ARG="record", A="name", B="score", SAMPLE="('Ada', 1200)", EXPECT="'Ada: 1200'"),
    dict(NAME="label", ARG="pair", A="symbol", B="price", SAMPLE="('BTC', 68000)", EXPECT="'BTC: 68000'"),
    dict(NAME="line", ARG="row", A="player", B="wins", SAMPLE="('Byte', 3)", EXPECT="'Byte: 3'"),
]

STARTER = '''
def @NAME@(@ARG@):
    @A@ = @ARG@[0]
    @B@ = @ARG@[1]
    return f"{@A@}: {@B@}"
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    @A@, @B@ = @ARG@
    return f"{@A@}: {@B@}"
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_list_input(ns, check):
    check(ns["@NAME@"](["x", 1]), "x: 1", "a two-item list unpacks the same way")

def test_unpacking(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no indexing left")
    check(ast_tools.count_nodes(src, "Tuple") >= 1, True, "tuple unpacking is used")
'''
