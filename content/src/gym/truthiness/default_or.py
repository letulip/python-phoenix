META = dict(
    id="gym.truthiness.default-or", type="cloze", order=50,
    difficulty=1, minutes=1, world="game",
    concepts=["truthiness", "ternary"],
    title="A default with or",
    statement_en="Fill in the operator so that an empty or missing name falls back to '@DEFAULT@'. The blank is a single keyword.",
    hints_en=["'x or y' gives x when x is truthy and y otherwise. An empty string and None are both falsy."],
    hints_ru=["x or y даёт x, если x истинно, иначе y. Пустая строка и None оба ложны."],
    explanation_en="'value or default' is the one-line fallback for empty and None at once. Know its edge: it also replaces 0 and '', so when 0 is a real value, use 'x if x is not None else default' instead.",
    explanation_ru="value or default – однострочный запасной вариант сразу для пустого и None. Знай его край: он заменяет и 0, и '', так что когда 0 – настоящее значение, пиши x if x is not None else default.",
)

VARIANTS = [
    dict(DEFAULT="stranger"),
    dict(DEFAULT="anon"),
    dict(DEFAULT="friend"),
]

STARTER = '''
def greet(name):
    shown = name ___ "@DEFAULT@"      # an empty or missing name falls back
    return f"Hi, {shown}!"

# greet("Ann") -> "Hi, Ann!",  greet("") -> "Hi, @DEFAULT@!",  greet(None) -> "Hi, @DEFAULT@!"
'''

SOLUTION = '''
def greet(name):
    shown = name or "@DEFAULT@"
    return f"Hi, {shown}!"
'''

TESTS = '''
def test_named(ns, check):
    check(ns["greet"]("Ann"), "Hi, Ann!", "greet('Ann')")

def test_empty_and_none(ns, check):
    check((ns["greet"](""), ns["greet"](None)), ("Hi, @DEFAULT@!", "Hi, @DEFAULT@!"), "greet('') and greet(None)")

def test_uses_or(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "Or") >= 1, True, "uses 'or'")
'''
