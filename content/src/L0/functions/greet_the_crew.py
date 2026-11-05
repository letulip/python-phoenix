META = dict(
    id="l0.functions.greet-the-crew", type="retype", order=10,
    difficulty=1, minutes=3, world="game",
    concepts=["def-return", "default-args", "docstring", "call-function"],
    story_en="Captain Byte's parrot used to greet the crew. The parrot retired. You are the parrot now.",
    title="Greet the crew",
    statement_en=("Captain Byte's ship greets every new crew member. Retype the snippet exactly as shown: "
                  "a function with a docstring and a default argument, called twice. "
                  "Typing it by hand is the point – no pasting."),
    hints_en=["The default value lives in the def line: excitement=1. A string times a number repeats it: '!' * 3 is '!!!'."],
    hints_ru=["Умолчание живёт в строке def: excitement=1. Строка, умноженная на число, повторяется: '!' * 3 даёт '!!!'."],
    explanation_en=("greet returns a string instead of printing it, so the caller decides what to do with it. "
                    "The second call passes excitement by keyword, which reads better than a bare 3."),
    explanation_ru=("greet возвращает строку, а не печатает её, поэтому решает вызывающий код. "
                    "Во втором вызове excitement передан по имени: так читается лучше, чем голая тройка."),
)

MODEL = '''
def greet(name, excitement=1):
    """Return a greeting; more excitement means more exclamation marks."""
    return "Hello, " + name + "!" * excitement

print(greet("Pixel"))
print(greet("Captain Byte", excitement=3))
'''

STARTER = ""

TESTS = '''
def test_greet_default(ns, check):
    check(ns["greet"]("Pixel"), "Hello, Pixel!", "greet('Pixel')")

def test_greet_excited(ns, check):
    check(ns["greet"]("Captain Byte", excitement=3), "Hello, Captain Byte!!!", "greet('Captain Byte', excitement=3)")

def test_has_docstring(ns, check):
    check(bool(ns["greet"].__doc__), True, "greet has a docstring")

def test_printed_lines(stdout, check):
    check(stdout.strip().splitlines(), ["Hello, Pixel!", "Hello, Captain Byte!!!"], "printed lines")
'''
