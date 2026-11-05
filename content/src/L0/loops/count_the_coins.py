META = dict(
    id="l0.loops.count-the-coins", type="retype", order=10,
    difficulty=1, minutes=3, world="game",
    concepts=["for-loop", "accumulator", "range"],
    story_en="The belt counts Byte's coins so the first mate can stop using his toes.",
    title="Count the coins",
    statement_en="Retype the snippet: an accumulator loop over a list, then two loops over range with a step.",
    hints_en=["total starts at 0 before the loop. range(3, 0, -1) counts down and stops before 0; range(0, 10, 2) steps by two."],
    hints_ru=["total начинается с 0 до цикла. range(3, 0, -1) считает вниз и останавливается перед 0; range(0, 10, 2) идёт через два."],
    explanation_en="The accumulator pattern is the backbone of most loops: create the result before, update it inside, use it after. range with a negative step counts down and still excludes the stop value.",
    explanation_ru="Паттерн накопителя – основа большинства циклов: создай результат до, обновляй внутри, используй после. range с отрицательным шагом считает вниз и по-прежнему не включает stop.",
)

MODEL = '''
coins = [5, 10, 25, 10]
total = 0
for coin in coins:
    total += coin

countdown = []
for n in range(3, 0, -1):
    countdown.append(n)

evens = []
for n in range(0, 10, 2):
    evens.append(n)
'''

STARTER = ""

TESTS = '''
def test_total(ns, check):
    check(ns["total"], 50, "total")

def test_countdown(ns, check):
    check(ns["countdown"], [3, 2, 1], "countdown")

def test_evens(ns, check):
    check(ns["evens"], [0, 2, 4, 6, 8], "evens")
'''
