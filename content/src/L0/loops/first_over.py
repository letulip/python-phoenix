META = dict(
    id="l0.loops.first-over", type="task", order=68,
    difficulty=1, minutes=4, world="bybit",
    concepts=["enumerate", "for-loop", "early-return"],
    story_en="Dr. Candle wants to know the first minute the price crossed his line. Not every minute. Not a chart. The first one.",
    title="First price over the line",
    statement_en=("Write first_over(prices, limit) -> int: the index of the first price strictly greater than limit, or -1 "
                  "when no price qualifies. Use enumerate for the index; no manual counter."),
    hints_en=[
        "for index, price in enumerate(prices): gives you both the position and the value.",
        "Return the index as soon as price > limit; after the loop, return -1.",
    ],
    hints_ru=[
        "for index, price in enumerate(prices): даёт и позицию, и значение.",
        "Верни index, как только price > limit; после цикла верни -1.",
    ],
    explanation_en=("enumerate removes the counter you would otherwise maintain by hand, and returning from inside the "
                    "loop stops the search at the first hit. The return after the loop is the 'not found' path and runs "
                    "only when nothing matched."),
    explanation_ru=("enumerate убирает счётчик, который иначе пришлось бы вести руками, а return внутри цикла останавливает "
                    "поиск на первом совпадении. return после цикла – путь «не найдено», он выполняется только когда ничего "
                    "не подошло."),
    talk_track=[
        "Say enumerate gives index and value together, so no counter is needed.",
        "Mention the early return stops at the first match: O(n) worst case, often far less.",
    ],
    complexity="O(n) worst case",
    followups=["Why -1 and not None? Which would you choose in Python?", "How would you find the first price over the line after a given index?"],
)

STARTER = '''
def first_over(prices, limit):
    ...
'''

EXAMPLES = [
    {"call": "first_over([64000, 67500, 69100, 68000], 68000)", "expected": "2"},
    {"call": "first_over([1, 2], 5)", "expected": "-1"},
]

SOLUTION = '''
def first_over(prices, limit):
    for index, price in enumerate(prices):
        if price > limit:
            return index
    return -1
'''

TESTS = '''
def test_found(ns, check):
    check(ns["first_over"]([64000, 67500, 69100, 68000], 68000), 2, "first_over([64000, 67500, 69100, 68000], 68000)")

def test_not_found(ns, check):
    check(ns["first_over"]([1, 2], 5), -1, "first_over([1, 2], 5)")

def test_empty(ns, check):
    check(ns["first_over"]([], 5), -1, "first_over([], 5)")

def test_equal_does_not_count(ns, check):
    check(ns["first_over"]([5, 6], 5), 1, "5 is not over 5, 6 is")

def test_first_index(ns, check):
    check(ns["first_over"]([9, 1], 0), 0, "a hit at index 0")

def test_uses_enumerate(src, ast_tools, check):
    check(ast_tools.uses_name(src, "enumerate"), True, "enumerate is used")
'''

LEVELS = dict(
    middle=dict(
        code='''
def first_over(prices, limit):
    found = -1
    for index, price in enumerate(prices):
        if price > limit:
            found = index
            break
    return found
''',
        note_en=("enumerate instead of a hand counter: good. The found flag plus break is the long way to say 'return as "
                 "soon as you know': two extra lines and one more variable whose value the reader has to track to the "
                 "end. Nothing wrong, just not the direct form."),
        note_ru=("enumerate вместо ручного счётчика: хорошо. Флаг found плюс break – длинный способ сказать «вернись, как "
                 "только узнал»: две лишние строки и ещё одна переменная, значение которой читателю приходится держать "
                 "в голове до конца. Ошибки нет, просто не прямая форма."),
    ),
    senior=dict(
        code='''
def first_over(prices, limit):
    """Index of the first price strictly above `limit`, or -1."""
    return next((index for index, price in enumerate(prices) if price > limit), -1)
''',
        note_en=("next() with a default on a generator is the standard 'first match or fallback': it stops at the first "
                 "hit, allocates nothing and reads as the sentence it implements. A senior adds that the early-return "
                 "loop is the readable twin for a team that does not know next(), and that -1 for 'not found' is a C "
                 "habit: in Python None is the usual answer, so ask the caller which one they want."),
        note_ru=("next() с умолчанием поверх генератора – стандартное «первое совпадение или запасное значение»: "
                 "останавливается на первом попадании, ничего не выделяет и читается как фраза, которую реализует. Сеньор "
                 "добавит, что цикл с ранним return – читаемый близнец для команды, не знающей next(), а -1 для «не найдено» – "
                 "привычка из C: в Python обычный ответ None, так что спроси вызывающего, что ему нужно."),
    ),
)
