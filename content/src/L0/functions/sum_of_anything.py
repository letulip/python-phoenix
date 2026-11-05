META = dict(
    id="l0.functions.sum-of-anything", type="cloze", order=50,
    difficulty=1, minutes=2, world="neutral",
    concepts=["star-args", "def-return"],
    story_en="Pixel's accountant quit after being asked to add 'a few more numbers'. One character would have saved him.",
    title="Sum of anything",
    statement_en=("Fill in the blank so that total(1, 2, 3) returns 6, total(5) returns 5 and total() returns 0. "
                  "The blank is a single character."),
    hints_en=["One star before the parameter name collects all positional arguments into a tuple."],
    hints_ru=["Одна звёздочка перед именем параметра собирает все позиционные аргументы в кортеж."],
    explanation_en="*numbers makes the function variadic. With no arguments the tuple is empty, so the loop never runs and 0 comes back.",
    explanation_ru="*numbers делает функцию вариативной. Без аргументов кортеж пуст, цикл не выполняется и возвращается 0.",
)

STARTER = '''
def total(___numbers):
    result = 0
    for n in numbers:
        result += n
    return result

# total(1, 2, 3) -> 6    total(5) -> 5    total() -> 0
'''

SOLUTION = '''
def total(*numbers):
    result = 0
    for n in numbers:
        result += n
    return result
'''

TESTS = '''
def test_three(ns, check):
    check(ns["total"](1, 2, 3), 6, "total(1, 2, 3)")

def test_one(ns, check):
    check(ns["total"](5), 5, "total(5)")

def test_none(ns, check):
    check(ns["total"](), 0, "total()")
'''
