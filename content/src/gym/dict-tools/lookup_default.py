META = dict(
    id="gym.dict-tools.lookup-default", type="rewrite", order=30,
    difficulty=1, minutes=1, world="bybit",
    concepts=["dict-get", "in-operator"],
    title="Lookup with a default",
    statement_en="@NAME@(@ARG@, @KEY@) checks 'in' and then indexes, or returns a default. Rewrite the body as one return with dict.get: no if statement and no indexing may remain.",
    hints_en=["@ARG@.get(@KEY@, @DEFAULT@) is the whole body: the value when the key exists, @DEFAULT@ otherwise."],
    hints_ru=["@ARG@.get(@KEY@, @DEFAULT@) – всё тело: значение, если ключ есть, иначе @DEFAULT@."],
    explanation_en="'in' followed by [] looks the key up twice and takes four lines; get does one lookup and says the default right where it is used.",
    explanation_ru="in, а затем [] ищут ключ дважды и занимают четыре строки; get ищет один раз и называет умолчание там же, где оно используется.",
)

VARIANTS = [
    dict(NAME="balance_of", ARG="wallets", KEY="name", DEFAULT="0", SAMPLE="{'ada': 50}", KNOWN="'ada'", KNOWN_VALUE="50", UNKNOWN="'byte'"),
    dict(NAME="price_of", ARG="prices", KEY="symbol", DEFAULT="None", SAMPLE="{'BTC': 68000}", KNOWN="'BTC'", KNOWN_VALUE="68000", UNKNOWN="'DOGE'"),
    dict(NAME="rating_of", ARG="ratings", KEY="player", DEFAULT="1000", SAMPLE="{'Byte': 1450}", KNOWN="'Byte'", KNOWN_VALUE="1450", UNKNOWN="'Ada'"),
]

STARTER = '''
def @NAME@(@ARG@, @KEY@):
    if @KEY@ in @ARG@:
        return @ARG@[@KEY@]
    return @DEFAULT@
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@, @KNOWN@)", "expected": "@KNOWN_VALUE@"},
    {"call": "@NAME@(@SAMPLE@, @UNKNOWN@)", "expected": "@DEFAULT@"},
]

SOLUTION = '''
def @NAME@(@ARG@, @KEY@):
    return @ARG@.get(@KEY@, @DEFAULT@)
'''

TESTS = '''
def test_known_and_unknown(ns, check):
    check((ns["@NAME@"](@SAMPLE@, @KNOWN@), ns["@NAME@"](@SAMPLE@, @UNKNOWN@)), (@KNOWN_VALUE@, @DEFAULT@), "known key, unknown key")

def test_get(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "If"), 0, "no if statement left")
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no indexing left")
    check(ast_tools.count_calls(src, "get") >= 1, True, "dict.get is used")
'''
