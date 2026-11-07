META = dict(
    id="gym.join.numbered-block", type="rewrite", order=20,
    difficulty=2, minutes=2, world="everyday",
    concepts=["split-join", "f-string", "enumerate"],
    title="Numbered lines without + and rstrip",
    statement_en="@NAME@(@ARG@) builds a numbered block by adding strings together and then strips the last newline. Rewrite it with an f-string per line, enumerate for the numbers and '\\n'.join for the block: no + on strings, no += and no rstrip may remain.",
    hints_en=["'\\n'.join(f'{number}. {item}' for number, item in enumerate(@ARG@, start=1)) is the whole body."],
    hints_ru=["'\\n'.join(f'{number}. {item}' for number, item in enumerate(@ARG@, start=1)) – это всё тело функции."],
    explanation_en="Three idioms in one line: enumerate numbers the items, the f-string formats a line, join glues the lines with newlines only between them, so the rstrip disappears with the trailing newline.",
    explanation_ru="Три идиомы в одной строке: enumerate нумерует элементы, f-строка форматирует строку, join склеивает строки переводами только между ними, и rstrip исчезает вместе с хвостовым переводом строки.",
)

VARIANTS = [
    dict(NAME="numbered", ARG="items", SAMPLE="['rope', 'lamp']", EXPECT="'1. rope\\n2. lamp'"),
    dict(NAME="checklist", ARG="steps", SAMPLE="['stretch', 'serve', 'rest']", EXPECT="'1. stretch\\n2. serve\\n3. rest'"),
    dict(NAME="agenda", ARG="topics", SAMPLE="['intro']", EXPECT="'1. intro'"),
]

STARTER = '''
def @NAME@(@ARG@):
    text = ""
    number = 1
    for item in @ARG@:
        text = text + str(number) + ". " + item + "\\n"
        number += 1
    return text.rstrip("\\n")
'''

EXAMPLES = [
    {"call": "@NAME@(@SAMPLE@)", "expected": "@EXPECT@"},
]

SOLUTION = '''
def @NAME@(@ARG@):
    return "\\n".join(f"{number}. {item}" for number, item in enumerate(@ARG@, start=1))
'''

TESTS = '''
def test_sample(ns, check):
    check(ns["@NAME@"](@SAMPLE@), @EXPECT@, "@NAME@(@SAMPLE@)")

def test_empty(ns, check):
    check(ns["@NAME@"]([]), "", "@NAME@([])")

def test_idioms(src, ast_tools, check):
    check(ast_tools.count_calls(src, "join") >= 1, True, "join is used")
    check(ast_tools.uses_name(src, "enumerate"), True, "enumerate is used")
    check(ast_tools.count_fstrings(src) >= 1, True, "an f-string is used")
    check(ast_tools.count_nodes(src, "Add") + ast_tools.count_nodes(src, "AugAssign"), 0, "no string addition left")
    check(ast_tools.count_calls(src, "rstrip"), 0, "no rstrip left")
'''
