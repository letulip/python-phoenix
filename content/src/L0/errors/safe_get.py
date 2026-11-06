META = dict(
    id="l0.errors.safe-get", type="task", order=64,
    difficulty=2, minutes=6, world="bybit",
    concepts=["try-except", "key-error", "dict-get", "eafp-lbyl"],
    story_en="The exchange answers with a dict inside a dict inside a dict. Some nights a level is missing. Dr. Candle's bot used to dig anyway and hit bedrock.",
    title="Safe nested lookup",
    statement_en=("Write safe_get(data, path, default=None). data is a nested structure of dicts and path is a list of "
                  "string keys. Follow the keys one by one and return the value at the end. If a key is missing, or the "
                  "value on the way is not a dict while keys remain, return default instead. An empty path returns data "
                  "itself."),
    hints_en=[
        "Walk with a loop: current = data, then current = current[key] for each key.",
        "Two things can go wrong: KeyError (missing key) and TypeError (current is not subscriptable). Catch both.",
        "Return default from inside the except; after the loop return current.",
    ],
    hints_ru=[
        "Иди циклом: current = data, затем current = current[key] для каждого ключа.",
        "Сломаться могут две вещи: KeyError (нет ключа) и TypeError (current нельзя индексировать). Лови обе.",
        "Верни default прямо из except; после цикла верни current.",
    ],
    explanation_en=("EAFP: attempt the lookup and catch the two ways it fails, instead of inspecting the type and the key "
                    "before every step. The happy path stays one indented line, and the function works for any mapping, "
                    "not only dict."),
    explanation_ru=("EAFP: попробовать обращение и поймать два способа, которыми оно ломается, вместо проверки типа и "
                    "ключа перед каждым шагом. Счастливый путь остаётся одной строкой, а функция работает с любым "
                    "отображением, не только с dict."),
    talk_track=[
        "Name the two failure modes: a missing key and a non-dict in the middle of the path.",
        "Say EAFP keeps the happy path flat; LBYL would check isinstance and 'in' at every step.",
        "Complexity O(len(path)).",
    ],
    complexity="O(k) for k keys in the path",
    followups=["Should an int key into a list on the way be allowed?", "How would you write it recursively, and would you?"],
)

STARTER = '''
def safe_get(data, path, default=None):
    ...
'''

EXAMPLES = [
    {"call": "safe_get({'ticker': {'BTC': {'last': 68000}}}, ['ticker', 'BTC', 'last'])", "expected": "68000"},
    {"call": "safe_get({'ticker': {}}, ['ticker', 'ETH', 'last'], 0)", "expected": "0"},
]

SOLUTION = '''
def safe_get(data, path, default=None):
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, TypeError):
            return default
    return current
'''

TESTS = '''
DATA = {"ticker": {"BTC": {"last": 68000, "bid": 67990}}, "status": "ok"}

def test_found(ns, check):
    check(ns["safe_get"](DATA, ["ticker", "BTC", "last"]), 68000, "safe_get(DATA, ['ticker', 'BTC', 'last'])")

def test_missing_key(ns, check):
    check(ns["safe_get"](DATA, ["ticker", "ETH", "last"]), None, "missing coin gives None")

def test_custom_default(ns, check):
    check(ns["safe_get"](DATA, ["ticker", "ETH", "last"], 0), 0, "missing coin gives the default")

def test_not_a_dict_on_the_way(ns, check):
    check(ns["safe_get"](DATA, ["status", "code"], "n/a"), "n/a", "a string in the middle of the path")

def test_empty_path(ns, check):
    check(ns["safe_get"](DATA, []) is DATA, True, "empty path returns data itself")

def test_partial_path(ns, check):
    check(ns["safe_get"](DATA, ["ticker", "BTC"]), {"last": 68000, "bid": 67990}, "a path ending at a dict returns that dict")
'''

LEVELS = dict(
    middle=dict(
        code='''
def safe_get(data, path, default=None):
    current = data
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
''',
        note_en=("Look before you leap: the isinstance-and-in check is explicit, easy to read and correct. Its weakness is "
                 "that it bakes in 'dict' and 'in': a Mapping that is not a dict, or an object with __getitem__, fails "
                 "the check although the lookup would work. When the interviewer asks 'why not try/except', the answer "
                 "should be a comparison, not a shrug."),
        note_ru=("Проверка перед прыжком: isinstance плюс in – явно, легко читается и верно. Слабость в том, что сюда "
                 "вшиты именно dict и in: отображение, которое не dict, или объект с __getitem__ не пройдут проверку, "
                 "хотя обращение сработало бы. Когда интервьюер спросит «почему не try/except», ответом должно быть "
                 "сравнение, а не пожатие плечами."),
    ),
    senior=dict(
        code='''
def safe_get(data, path, default=None):
    """Value at the nested `path` of keys, or `default` when the path breaks."""
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, TypeError):
            return default
    return current
''',
        note_en=("EAFP: attempt the lookup and catch exactly the two ways it fails, a missing key and a non-subscriptable "
                 "value. It works for any mapping and keeps the happy path unindented. A senior names the trade-off, "
                 "EAFP wins when failures are rare and LBYL reads better when they are the norm, and mentions "
                 "functools.reduce or recursion as alternatives they chose not to write."),
        note_ru=("EAFP: попробовать обращение и поймать ровно два способа провала – отсутствующий ключ и значение, которое "
                 "нельзя индексировать. Работает с любым отображением и держит счастливый путь без отступов. Сеньор "
                 "называет компромисс: EAFP выигрывает, когда провалы редки, а LBYL читается лучше, когда они норма, и "
                 "упоминает functools.reduce или рекурсию как варианты, которые сознательно не стал писать."),
    ),
)
