META = dict(
    id="l0.comprehensions.comprehension-trio", type="retype", order=10,
    difficulty=1, minutes=3, world="tennis",
    concepts=["list-comprehension", "dict-comprehension", "set-comprehension", "comprehension-if"],
    story_en="Coach Topspin wants the passing scores, everything doubled 'for motivation', a yes/no table and the tens digits. All before lunch.",
    title="Comprehension trio",
    statement_en="Retype the snippet: a filtering list comprehension, a transforming one, a dict comprehension and a set comprehension.",
    hints_en=["Square brackets make a list, curly braces with key: value make a dict, curly braces without a colon make a set."],
    hints_ru=["Квадратные скобки дают список, фигурные с key: value – словарь, фигурные без двоеточия – множество."],
    explanation_en="The same three-part shape builds all three: expression, for clause, optional if. The brackets decide the container; the set collapses duplicates, which is why tens has five members here but would have fewer with repeated digits.",
    explanation_ru="Одна и та же трёхчастная форма строит все три: выражение, часть for, необязательный if. Скобки определяют контейнер; множество схлопывает дубликаты, поэтому tens здесь из пяти элементов, а при повторах было бы меньше.",
)

MODEL = '''
scores = [61, 48, 75, 90, 33]
passed = [s for s in scores if s >= 50]
doubled = [s * 2 for s in scores]
by_score = {s: s >= 50 for s in scores}
tens = {s // 10 for s in scores}
'''

STARTER = ""

TESTS = '''
def test_passed(ns, check):
    check(ns["passed"], [61, 75, 90], "passed")

def test_doubled(ns, check):
    check(ns["doubled"], [122, 96, 150, 180, 66], "doubled")

def test_by_score(ns, check):
    check(ns["by_score"], {61: True, 48: False, 75: True, 90: True, 33: False}, "by_score")

def test_tens(ns, check):
    check(ns["tens"], {6, 4, 7, 9, 3}, "tens")
'''
