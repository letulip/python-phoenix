META = dict(
    id="l0.loops.meow-purr", type="task", order=60,
    difficulty=1, minutes=5, world="game",
    concepts=["for-loop", "range", "ternary"],
    story_en="Pixel's team-building game: count up, but every third number is Meow and every fifth is Purr. The intern never gets 15 right.",
    title="Meow-Purr",
    statement_en=("Write meow_purr(n) -> list[str]. For each number from 1 to n inclusive append 'Meow' if it is divisible by 3, "
                  "'Purr' if divisible by 5, 'MeowPurr' if divisible by both, otherwise the number itself as a string. "
                  "meow_purr(0) is an empty list."),
    hints_en=[
        "Loop with range(1, n + 1); the + 1 is the classic trap.",
        "Check 'divisible by both' first, or build the word from parts: start with '', add 'Meow', add 'Purr', fall back to str(i).",
        "Every element must be a string, so plain numbers go through str(i).",
    ],
    hints_ru=[
        "Цикл по range(1, n + 1); + 1 – классическая ловушка.",
        "Проверяй «делится на оба» первым или собирай слово из частей: начни с '', добавь 'Meow', добавь 'Purr', иначе str(i).",
        "Каждый элемент должен быть строкой, поэтому обычные числа идут через str(i).",
    ],
    explanation_en=("The order of checks matters: 15 must become 'MeowPurr', so either test 15 first or build the word from "
                    "parts. Building from parts scales to a third word without rewriting the chain."),
    explanation_ru=("Порядок проверок важен: 15 должно стать 'MeowPurr', поэтому либо проверяй 15 первым, либо собирай слово из "
                    "частей. Сборка из частей масштабируется на третье слово без переписывания цепочки."),
    talk_track=[
        "Mention the 15 case must be handled first or built from parts.",
        "Say range(1, n + 1) includes n.",
        "Complexity is O(n), trivially.",
    ],
    complexity="O(n)",
    followups=["Make the words and divisors configurable.", "How would you write it as a generator?"],
)

STARTER = '''
def meow_purr(n):
    ...
'''

EXAMPLES = [
    {"call": "meow_purr(5)", "expected": "['1', '2', 'Meow', '4', 'Purr']"},
    {"call": "meow_purr(0)", "expected": "[]"},
]

SOLUTION = '''
def meow_purr(n):
    result = []
    for i in range(1, n + 1):
        word = ""
        if i % 3 == 0:
            word += "Meow"
        if i % 5 == 0:
            word += "Purr"
        result.append(word if word else str(i))
    return result
'''

TESTS = '''
def test_five(ns, check):
    check(ns["meow_purr"](5), ["1", "2", "Meow", "4", "Purr"], "meow_purr(5)")

def test_fifteen(ns, check):
    check(ns["meow_purr"](15)[14], "MeowPurr", "meow_purr(15)[14]")

def test_zero(ns, check):
    check(ns["meow_purr"](0), [], "meow_purr(0)")

def test_length(ns, check):
    check(len(ns["meow_purr"](100)), 100, "len(meow_purr(100))")

def test_all_strings(ns, check):
    check(all(isinstance(x, str) for x in ns["meow_purr"](20)), True, "every element is a str")

def test_three(ns, check):
    check(ns["meow_purr"](3), ["1", "2", "Meow"], "meow_purr(3)")
'''
