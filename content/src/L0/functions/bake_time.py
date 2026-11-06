META = dict(
    id="l0.functions.bake-time", type="task", order=64,
    difficulty=1, minutes=5, world="everyday",
    concepts=["default-args", "early-return", "def-return"],
    story_en="Grandma Ada's oven takes two trays at a time. She wants to know when the bread is done, not a lecture about ovens.",
    title="Bake time",
    statement_en=("Write bake_time(loaves, minutes_each=25, oven_slots=2) -> int. The oven bakes up to oven_slots loaves at "
                  "once and every batch takes minutes_each minutes, so the answer is the number of batches times "
                  "minutes_each. Zero loaves take zero minutes. Callers may pass the extra arguments by name."),
    hints_en=[
        "Zero loaves is the special case: return 0 before any division.",
        "The number of batches is loaves divided by oven_slots, rounded up: (loaves + oven_slots - 1) // oven_slots.",
        "Multiply the batches by minutes_each and return an int; do not use float division.",
    ],
    hints_ru=[
        "Ноль буханок – особый случай: верни 0 до любого деления.",
        "Число партий – loaves, делённое на oven_slots с округлением вверх: (loaves + oven_slots - 1) // oven_slots.",
        "Умножь партии на minutes_each и верни int; дробное деление не используй.",
    ],
    explanation_en=("Default arguments give the common case a one-argument call while keeping the oven configurable. "
                    "The ceiling trick (a + b - 1) // b avoids floats and math.ceil, and the early return for zero loaves "
                    "keeps the main formula free of special cases."),
    explanation_ru=("Аргументы по умолчанию дают обычному случаю вызов с одним аргументом, а печь остаётся настраиваемой. "
                    "Трюк округления вверх (a + b - 1) // b обходится без float и math.ceil, а ранний return для нуля "
                    "буханок оставляет основную формулу без особых случаев."),
    talk_track=[
        "Say the batches are a ceiling division and show the integer trick.",
        "Point out the defaults keep the common call short while the oven stays configurable.",
        "Mention the zero case and that the result is an int.",
    ],
    complexity="O(1)",
    followups=["What should happen with oven_slots=0 or a negative loaf count?", "How would you return the finishing time of day instead?"],
)

STARTER = '''
def bake_time(loaves, minutes_each=25, oven_slots=2):
    ...
'''

EXAMPLES = [
    {"call": "bake_time(4)", "expected": "50"},
    {"call": "bake_time(5)", "expected": "75"},
    {"call": "bake_time(3, 30, oven_slots=3)", "expected": "30"},
]

SOLUTION = '''
def bake_time(loaves, minutes_each=25, oven_slots=2):
    if loaves == 0:
        return 0
    batches = (loaves + oven_slots - 1) // oven_slots
    return batches * minutes_each
'''

TESTS = '''
def test_two_batches(ns, check):
    check(ns["bake_time"](4), 50, "bake_time(4)")

def test_rounds_up(ns, check):
    check(ns["bake_time"](5), 75, "bake_time(5): five loaves need three batches")

def test_zero(ns, check):
    check(ns["bake_time"](0), 0, "bake_time(0)")

def test_custom_oven(ns, check):
    check(ns["bake_time"](3, 30, oven_slots=3), 30, "bake_time(3, 30, oven_slots=3)")

def test_keyword_call(ns, check):
    check(ns["bake_time"](2, oven_slots=1), 50, "bake_time(2, oven_slots=1)")

def test_returns_int(ns, check):
    check(type(ns["bake_time"](7)), int, "type(bake_time(7))")
'''

LEVELS = dict(
    middle=dict(
        code='''
import math

def bake_time(loaves, minutes_each=25, oven_slots=2):
    if loaves == 0:
        return 0
    batches = math.ceil(loaves / oven_slots)
    return batches * minutes_each
''',
        note_en=("Correct, and math.ceil says 'round up' in plain words, which is good. The division goes through float, "
                 "so for huge counts the result can drift, and the function has no opinion about oven_slots=0: it just "
                 "crashes with ZeroDivisionError somewhere the caller did not expect. An interviewer will ask about that "
                 "case, so have the answer ready."),
        note_ru=("Верно, и math.ceil прямо говорит «округли вверх», это плюс. Но деление идёт через float, на огромных числах "
                 "результат может поплыть, а про oven_slots=0 у функции нет мнения: она просто падает с ZeroDivisionError там, "
                 "где вызывающий не ждал. Интервьюер спросит про этот случай, так что ответ лучше иметь заранее."),
    ),
    senior=dict(
        code='''
def bake_time(loaves, minutes_each=25, oven_slots=2):
    """Minutes to bake `loaves` when the oven takes `oven_slots` loaves per batch."""
    if oven_slots <= 0:
        raise ValueError("oven_slots must be positive")
    if loaves <= 0:
        return 0
    batches = -(-loaves // oven_slots)
    return batches * minutes_each
''',
        note_en=("States the contract first: a zero-slot oven is a ValueError with a message, not a crash three frames "
                 "deeper. The integer ceiling -(-a // b) stays in int arithmetic; a senior knows the idiom and also knows "
                 "to say 'I would use (a + b - 1) // b or a comment if the team finds this cryptic'. Negative loaves are "
                 "treated as zero on purpose, and the docstring says what the function promises."),
        note_ru=("Сначала контракт: печь без слотов – ValueError с сообщением, а не падение тремя кадрами глубже. Целочисленное "
                 "округление вверх -(-a // b) остаётся в int; сеньор знает идиому и знает сказать: «возьму (a + b - 1) // b "
                 "или комментарий, если команде это кажется загадкой». Отрицательные буханки сознательно считаются нулём, "
                 "а докстринг говорит, что функция обещает."),
    ),
)
