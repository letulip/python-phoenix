META = dict(
    id="l0.strings.initials", type="cloze", order=50,
    difficulty=1, minutes=2, world="tennis",
    concepts=["split-join", "string-slicing", "str-case"],
    story_en="Coach Topspin's scoreboard has room for three letters per player. Names like 'Bartholomew' are a problem; initials are the fix.",
    title="Initials",
    statement_en="Fill in the blanks so initials('ada byte lovelace') returns 'ABL'. Extra spaces between names must not matter.",
    hints_en=["split() with no argument handles any amount of whitespace. The first character of a string is index 0."],
    hints_ru=["split() без аргумента справляется с любым количеством пробелов. Первый символ строки – индекс 0."],
    explanation_en="split() without arguments is the robust word splitter: it ignores leading, trailing and repeated spaces. part[0] is the first letter, upper() makes it an initial.",
    explanation_ru="split() без аргументов – надёжный разрезатель на слова: он игнорирует пробелы в начале, в конце и повторы. part[0] – первая буква, upper() делает из неё инициал.",
)

STARTER = '''
def initials(full_name):
    parts = full_name.___()
    result = ""
    for part in parts:
        result += part[___].upper()
    return result

# initials("ada byte lovelace") -> "ABL"
'''

SOLUTION = '''
def initials(full_name):
    parts = full_name.split()
    result = ""
    for part in parts:
        result += part[0].upper()
    return result
'''

TESTS = '''
def test_three_names(ns, check):
    check(ns["initials"]("ada byte lovelace"), "ABL", "initials('ada byte lovelace')")

def test_single(ns, check):
    check(ns["initials"]("pixel"), "P", "initials('pixel')")

def test_messy_spaces(ns, check):
    check(ns["initials"]("  coach   topspin "), "CT", "initials('  coach   topspin ')")
'''
