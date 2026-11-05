META = dict(
    id="l0.loops.steps-to-one", type="cloze", order=50,
    difficulty=2, minutes=3, world="neutral",
    concepts=["while-loop", "ternary", "accumulator"],
    story_en="A mathematician left this on the belt in 1937. Nobody has proven it always stops. Yours will, for small numbers.",
    title="Steps to one",
    statement_en=("Fill in the blanks: repeat while n is above 1, halving even numbers and turning odd ones into 3n + 1, "
                  "counting the steps. steps_to_one(6) is 8 and steps_to_one(1) is 0."),
    hints_en=["The loop keyword for 'repeat while a condition holds' is while. Counting a step is steps += 1."],
    hints_ru=["Ключевое слово для «повторять, пока условие верно» – while. Засчитать шаг – steps += 1."],
    explanation_en="while is the loop for 'until something happens' when you cannot know the count in advance. The one-line conditional picks the next value without an if/else block.",
    explanation_ru="while – цикл «пока что-то не случится», когда число итераций заранее неизвестно. Однострочное условие выбирает следующее значение без блока if/else.",
)

STARTER = '''
def steps_to_one(n):
    steps = 0
    ___ n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps ___ 1
    return steps
# steps_to_one(6) -> 8, steps_to_one(1) -> 0, steps_to_one(7) -> 16
'''

SOLUTION = '''
def steps_to_one(n):
    steps = 0
    while n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
'''

TESTS = '''
def test_six(ns, check):
    check(ns["steps_to_one"](6), 8, "steps_to_one(6)")

def test_one(ns, check):
    check(ns["steps_to_one"](1), 0, "steps_to_one(1)")

def test_seven(ns, check):
    check(ns["steps_to_one"](7), 16, "steps_to_one(7)")

def test_two(ns, check):
    check(ns["steps_to_one"](2), 1, "steps_to_one(2)")
'''
