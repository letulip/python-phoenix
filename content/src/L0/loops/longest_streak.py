META = dict(
    id="l0.loops.longest-streak", type="task", order=64,
    difficulty=2, minutes=6, world="tennis",
    concepts=["for-loop", "accumulator", "ternary"],
    story_en="Coach Topspin pins the season on the wall as a row of W and L. He wants one number for the poster: the longest winning streak. Losses reset it. Coach knows all about resets.",
    title="Longest winning streak",
    statement_en=("Write longest_win_streak(results) -> int. results is a list of 'W' and 'L' strings in match order. "
                  "Return the length of the longest run of consecutive 'W'. No wins, or an empty list, gives 0."),
    hints_en=[
        "Two counters: current (the run you are in) and best (the longest run so far).",
        "A 'W' adds one to current, an 'L' resets it to 0; after every step best = max(best, current).",
        "Return best; the empty list never enters the loop and returns 0 on its own.",
    ],
    hints_ru=[
        "Два счётчика: current (серия, в которой ты сейчас) и best (самая длинная серия на данный момент).",
        "'W' прибавляет единицу к current, 'L' сбрасывает его в 0; после каждого шага best = max(best, current).",
        "Верни best; пустой список не входит в цикл и сам даёт 0.",
    ],
    explanation_en=("The accumulator pattern with a twist: one counter grows and resets, another remembers the maximum. "
                    "Updating best after every step, not only on a loss, is what makes a streak at the very end count."),
    explanation_ru=("Паттерн накопителя с поворотом: один счётчик растёт и сбрасывается, другой помнит максимум. "
                    "Обновление best после каждого шага, а не только при поражении, и даёт засчитать серию в самом конце."),
    talk_track=[
        "Say there are two counters: the current run and the best run.",
        "Point out the trap: a streak at the end counts only if best is updated inside the loop.",
        "Complexity O(n), O(1) memory.",
    ],
    complexity="O(n) time, O(1) space",
    followups=["Return the start index of the longest streak as well.", "What should happen with a value other than 'W' or 'L'?"],
)

STARTER = '''
def longest_win_streak(results):
    ...
'''

EXAMPLES = [
    {"call": "longest_win_streak(['W', 'W', 'L', 'W', 'W', 'W'])", "expected": "3"},
    {"call": "longest_win_streak(['L', 'L'])", "expected": "0"},
]

SOLUTION = '''
def longest_win_streak(results):
    best = 0
    current = 0
    for result in results:
        current = current + 1 if result == "W" else 0
        best = max(best, current)
    return best
'''

TESTS = '''
def test_middle_and_end(ns, check):
    check(ns["longest_win_streak"](["W", "W", "L", "W", "W", "W"]), 3, "longest_win_streak(['W', 'W', 'L', 'W', 'W', 'W'])")

def test_no_wins(ns, check):
    check(ns["longest_win_streak"](["L", "L"]), 0, "longest_win_streak(['L', 'L'])")

def test_empty(ns, check):
    check(ns["longest_win_streak"]([]), 0, "longest_win_streak([])")

def test_all_wins(ns, check):
    check(ns["longest_win_streak"](["W"] * 5), 5, "five wins in a row")

def test_single(ns, check):
    check(ns["longest_win_streak"](["W"]), 1, "longest_win_streak(['W'])")

def test_streak_at_the_end(ns, check):
    check(ns["longest_win_streak"](["L", "W", "W"]), 2, "a streak that ends the season still counts")

def test_returns_int(ns, check):
    check(type(ns["longest_win_streak"](["W", "L"])), int, "type of the result")
'''

LEVELS = dict(
    middle=dict(
        code='''
def longest_win_streak(results):
    best = 0
    current = 0
    for result in results:
        if result == "W":
            current += 1
            if current > best:
                best = current
        else:
            current = 0
    return best
''',
        note_en=("Two counters, reset on a loss, best updated inside the loop: the logic is exactly right, including the "
                 "streak-at-the-end trap. The nested if is the only thing a reviewer trims: max(best, current) after every "
                 "step says the same in one line and cannot be forgotten on one branch."),
        note_ru=("Два счётчика, сброс на поражении, best обновляется внутри цикла: логика ровно верная, включая ловушку с "
                 "серией в конце. Ревьюер подрежет только вложенный if: max(best, current) после каждого шага говорит то же "
                 "одной строкой, и его нельзя забыть в одной из веток."),
    ),
    senior=dict(
        code='''
from itertools import groupby

def longest_win_streak(results):
    """Length of the longest run of consecutive 'W'."""
    runs = (len(list(group)) for value, group in groupby(results) if value == "W")
    return max(runs, default=0)
''',
        note_en=("Sees the problem as 'runs' and asks the library for them: groupby splits the sequence into runs of equal "
                 "values, the generator keeps the W runs, max with default=0 covers the empty case. A senior says the "
                 "two-counter loop is just as good and O(1) in memory; the point is naming the concept. They also ask "
                 "whether anything but 'W' and 'L' can appear before promising anything."),
        note_ru=("Видит задачу как «серии» и просит их у библиотеки: groupby режет последовательность на серии одинаковых "
                 "значений, генератор оставляет серии W, max с default=0 закрывает пустой случай. Сеньор говорит, что цикл "
                 "с двумя счётчиками ничуть не хуже и O(1) по памяти; суть в том, чтобы назвать понятие. И спрашивает, может "
                 "ли прийти что-то кроме 'W' и 'L', прежде чем что-либо обещать."),
    ),
)
