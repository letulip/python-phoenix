META = dict(
    id="gym.guards.nested-ifs", type="rewrite", order=10,
    difficulty=2, minutes=2, world="game",
    concepts=["early-return"],
    title="Flatten the nested ifs",
    statement_en="@NAME@(user) answers through three nested if/else levels. Rewrite it with guard clauses: check the failing cases first, return at once, and finish with the success return. No if inside another if and no else may remain.",
    hints_en=['Order: if user is None: return ..., then if not user.get("active"): return ..., then the age check, then return "@OK@".'],
    hints_ru=['Порядок: if user is None: return ..., затем if not user.get("active"): return ..., затем проверка возраста, затем return "@OK@".'],
    explanation_en="Guard clauses turn a tree into a list: each line handles one way to fail and leaves. The reader never holds three open conditions in their head, and adding a fourth rule is one more line, not one more indent.",
    explanation_ru="Ранние return превращают дерево в список: каждая строка обрабатывает один способ провалиться и выходит. Читателю не нужно держать в голове три открытых условия, а четвёртое правило – ещё одна строка, а не ещё один отступ.",
)

VARIANTS = [
    dict(NAME="can_board", AGE="12", OK="welcome aboard"),
    dict(NAME="can_trade", AGE="18", OK="trade"),
    dict(NAME="can_drive", AGE="17", OK="keys"),
]

STARTER = '''
def @NAME@(user):
    if user is not None:
        if user.get("active"):
            if user.get("age", 0) >= @AGE@:
                return "@OK@"
            else:
                return "too young"
        else:
            return "inactive"
    else:
        return "no user"
'''

EXAMPLES = [
    {"call": "@NAME@({'active': True, 'age': 40})", "expected": "'@OK@'"},
    {"call": "@NAME@(None)", "expected": "'no user'"},
]

SOLUTION = '''
def @NAME@(user):
    if user is None:
        return "no user"
    if not user.get("active"):
        return "inactive"
    if user.get("age", 0) < @AGE@:
        return "too young"
    return "@OK@"
'''

TESTS = '''
def test_four_outcomes(ns, check):
    f = ns["@NAME@"]
    check((f(None), f({"active": False, "age": 40}), f({"active": True, "age": 3}), f({"active": True, "age": 40})),
          ("no user", "inactive", "too young", "@OK@"), "no user, inactive, too young, ok")

def test_missing_age(ns, check):
    check(ns["@NAME@"]({"active": True}), "too young", "a missing age counts as 0")

def test_flat(src, ast_tools, check):
    import ast
    tree = ast.parse(src)
    nested = any(isinstance(inner, ast.If) for node in ast.walk(tree) if isinstance(node, ast.If)
                 for inner in ast.walk(node) if inner is not node)
    check(nested, False, "no if inside another if")
    check(any(node.orelse for node in ast.walk(tree) if isinstance(node, ast.If)), False, "no else left")
'''
