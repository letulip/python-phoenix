META = dict(
    id="l0.collections.describe-crate", type="refactor", order=90,
    difficulty=2, minutes=6, world="game",
    concepts=["tuple-unpacking", "none-check", "truthiness"],
    story_en="Captain Byte's label printer was written in a hurry by the parrot. The parrot retired. The labels still come out right, which is the only nice thing anyone says about the code.",
    title="Unpack the crate label",
    statement_en=("describe_crate(crate) works but reads like a parrot wrote it: crate[0], crate[1], crate[2], "
                  "'== None' and 'len(kind) == 0'. Rewrite it with tuple unpacking into kind, amount and note, compare "
                  "with None using 'is', and use truthiness for the empty label. No indexing and no len() may remain. "
                  "Behaviour must not change."),
    hints_en=[
        "One line replaces three: kind, amount, note = crate.",
        "None is a single object, so the check is 'note is None'.",
        "An empty string is falsy: 'if not kind' replaces len(kind) == 0.",
    ],
    hints_ru=[
        "Одна строка вместо трёх: kind, amount, note = crate.",
        "None – единственный объект, поэтому проверка пишется как note is None.",
        "Пустая строка ложна: if not kind заменяет len(kind) == 0.",
    ],
    explanation_en=("Unpacking gives the parts names at the point where they enter the function, so the reader never "
                    "translates indexes in their head. 'is None' is the idiom because None is one object and == can be "
                    "overridden by other types. Truthiness turns a length check into the question you actually meant: "
                    "is there a label?"),
    explanation_ru=("Распаковка даёт частям имена там, где они входят в функцию, и читателю не нужно переводить индексы в "
                    "уме. is None – идиома, потому что None один, а == другие типы могут переопределить. Истинность "
                    "превращает проверку длины в вопрос, который ты и имел в виду: есть ли подпись?"),
    talk_track=[
        "Say unpacking names the parts where they arrive, so no index arithmetic is left in the body.",
        "Explain 'is None' versus '== None' in one sentence: identity of a singleton.",
        "Mention that an empty string being falsy is the whole reason 'if not kind' reads as intended.",
    ],
    complexity="O(1)",
    followups=["Would a namedtuple or dataclass for the crate be the next step? Why?", "What if the crate had four fields one day?"],
)

STARTER = '''
def describe_crate(crate):
    kind = crate[0]
    amount = crate[1]
    note = crate[2]
    if note == None:
        note = "no note"
    if len(kind) == 0:
        return "unlabelled crate"
    return f"{amount} x {kind} ({note})"
'''

EXAMPLES = [
    {"call": "describe_crate(('gold', 12, None))", "expected": "'12 x gold (no note)'"},
    {"call": "describe_crate(('', 3, 'fragile'))", "expected": "'unlabelled crate'"},
]

SOLUTION = '''
def describe_crate(crate):
    kind, amount, note = crate
    if note is None:
        note = "no note"
    if not kind:
        return "unlabelled crate"
    return f"{amount} x {kind} ({note})"
'''

TESTS = '''
def test_with_note(ns, check):
    check(ns["describe_crate"](("rum", 3, "fragile")), "3 x rum (fragile)", "describe_crate(('rum', 3, 'fragile'))")

def test_without_note(ns, check):
    check(ns["describe_crate"](("gold", 12, None)), "12 x gold (no note)", "describe_crate(('gold', 12, None))")

def test_unlabelled(ns, check):
    check(ns["describe_crate"](("", 3, "fragile")), "unlabelled crate", "empty kind")

def test_no_indexing_or_len(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no crate[i] indexing left")
    check(ast_tools.count_calls(src, "len"), 0, "no len() call left")

def test_unpacks_the_tuple(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "Tuple") >= 1, True, "the crate is unpacked into names")

def test_is_none(src, ast_tools, check):
    import ast
    eq_none = any(isinstance(node, ast.Compare)
                  and any(isinstance(op, ast.Eq) for op in node.ops)
                  and any(isinstance(c, ast.Constant) and c.value is None for c in node.comparators)
                  for node in ast.walk(ast.parse(src)))
    check(eq_none, False, "no '== None' left")
    check(ast_tools.count_nodes(src, "Is") >= 1, True, "compares with 'is None'")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Exactly the three substitutions the task asked for, in place, nothing else touched: that is a clean "
                 "refactor, and 'change nothing you were not asked to change' is a real virtue. The function still "
                 "reassigns note before checking whether the label exists at all, so the reader meets the default "
                 "before learning it may never be used."),
        note_ru=("Ровно три замены, которые просило задание, на месте, больше ничего не тронуто: это чистый рефакторинг, "
                 "и «не менять того, о чём не просили» – настоящее достоинство. Но функция всё ещё переназначает note "
                 "до проверки, есть ли подпись вообще, и читатель встречает умолчание раньше, чем узнаёт, что оно может "
                 "не понадобиться."),
    ),
    senior=dict(
        code='''
NO_NOTE = "no note"

def describe_crate(crate):
    """'<amount> x <kind> (<note>)', or 'unlabelled crate' when the kind is empty."""
    kind, amount, note = crate
    if not kind:
        return "unlabelled crate"
    return f"{amount} x {kind} ({NO_NOTE if note is None else note})"
''',
        note_en=("Guard first, then the one formatted line: the function reads top-down and the default note sits next to "
                 "the place it is used, with a name instead of a loose string. A senior also says what the real smell was: "
                 "a crate addressed by position. The next refactor would be a namedtuple or dataclass for the crate, and "
                 "they say 'next', because this task asked for this one."),
        note_ru=("Сначала защита, потом одна отформатированная строка: функция читается сверху вниз, а умолчание для note "
                 "стоит рядом с местом использования и носит имя вместо голой строки. Сеньор ещё называет настоящий запах: "
                 "ящик, к которому обращаются по позициям. Следующий рефакторинг – namedtuple или dataclass для ящика, и он "
                 "говорит «следующий», потому что это задание просило именно этот."),
    ),
)
