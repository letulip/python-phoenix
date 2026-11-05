META = dict(
    id="l0.comprehensions.any-all-check", type="retype", order=40,
    difficulty=1, minutes=2, world="tennis",
    concepts=["any-all", "comprehension-if"],
    story_en="Did every serve land? Was any serve fast? Coach Topspin asks yes/no questions and expects yes/no answers.",
    title="Any and all",
    statement_en="Retype the snippet: all over a list of booleans, any over a negated generator, and two generator checks on speeds.",
    hints_en=["any and all take an iterable; a generator expression inside the call needs no extra brackets."],
    hints_ru=["any и all принимают итерируемое; генераторному выражению внутри вызова лишние скобки не нужны."],
    explanation_en="any and all turn 'is there one' and 'is it true for every one' into a single readable call; both stop as soon as the answer is known.",
    explanation_ru="any и all превращают «есть ли хоть один» и «верно ли для всех» в один читаемый вызов; обе останавливаются, как только ответ известен.",
)

MODEL = '''
serves = [True, True, False, True]
all_in = all(serves)
any_fault = any(not s for s in serves)

speeds = [180, 195, 172]
fast = any(speed > 190 for speed in speeds)
slow_all = all(speed < 200 for speed in speeds)
'''

STARTER = ""

TESTS = '''
def test_serves(ns, check):
    check((ns["all_in"], ns["any_fault"]), (False, True), "all_in, any_fault")

def test_speeds(ns, check):
    check((ns["fast"], ns["slow_all"]), (True, True), "fast, slow_all")
'''
