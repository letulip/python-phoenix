META = dict(
    id="gym.truthiness.none-compare", type="rewrite", order=20,
    difficulty=1, minutes=1, world="everyday",
    concepts=["none-check"],
    title="is None, not == None",
    statement_en="@NAME@(@ARG@) compares with None using ==. Rewrite the comparison with 'is'. Behaviour must not change: 0 and '' are real values here, only None gets the default.",
    hints_en=["None is a single object, so the check is '@ARG@ is None'. Do not switch to 'if not @ARG@': that would also catch 0 and ''."],
    hints_ru=["None – единственный объект, поэтому проверка пишется как @ARG@ is None. Не меняй на if not @ARG@: это поймает ещё и 0 с ''."],
    explanation_en="'is None' checks identity with the one None object, which is both faster and immune to classes that override ==. Truthiness is a different question: 0 and '' are falsy but they are not None.",
    explanation_ru="is None проверяет тождество с единственным объектом None: это и быстрее, и не зависит от классов, переопределивших ==. Истинность – другой вопрос: 0 и '' ложны, но они не None.",
)

VARIANTS = [
    dict(NAME="label", ARG="note", DEFAULT="no note", VALUE="'fragile'"),
    dict(NAME="shown_name", ARG="name", DEFAULT="anonymous", VALUE="'Ada'"),
    dict(NAME="price_text", ARG="price", DEFAULT="n/a", VALUE="12.5"),
]

STARTER = '''
def @NAME@(@ARG@):
    if @ARG@ == None:
        return "@DEFAULT@"
    return @ARG@
'''

EXAMPLES = [
    {"call": "@NAME@(None)", "expected": "'@DEFAULT@'"},
    {"call": "@NAME@(@VALUE@)", "expected": "@VALUE@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    if @ARG@ is None:
        return "@DEFAULT@"
    return @ARG@
'''

TESTS = '''
def test_none_and_value(ns, check):
    check((ns["@NAME@"](None), ns["@NAME@"](@VALUE@)), ("@DEFAULT@", @VALUE@), "None and a real value")

def test_falsy_values_are_kept(ns, check):
    check((ns["@NAME@"](0), ns["@NAME@"]("")), (0, ""), "0 and '' are values, not None")

def test_is_none(src, ast_tools, check):
    import ast
    eq_none = any(isinstance(node, ast.Compare)
                  and any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops)
                  and any(isinstance(c, ast.Constant) and c.value is None for c in node.comparators)
                  for node in ast.walk(ast.parse(src)))
    check(eq_none, False, "no '== None' left")
    check(ast_tools.count_nodes(src, "Is") + ast_tools.count_nodes(src, "IsNot") >= 1, True, "compares with 'is'")
'''
