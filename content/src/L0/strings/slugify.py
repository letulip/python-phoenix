META = dict(
    id="l0.strings.slugify", type="task", order=70,
    difficulty=2, minutes=6, world="shorts",
    concepts=["split-join", "str-case", "str-methods"],
    story_en="Pixel's Shorts channel 'Emerald Lake' needs URL slugs. YouTube does not accept exclamation marks, however excited the title is.",
    title="Slugify a title",
    statement_en=("Write slugify(title) -> str: lowercase the title, replace every character that is not a letter or a digit "
                  "with a space, then join the words with single dashes. Leading, trailing and repeated spaces must not "
                  "produce dashes. An empty or symbols-only title gives ''."),
    hints_en=[
        "Lowercase first, then walk the characters: keep ch if ch.isalnum() else use a space.",
        "str.split() with no argument collapses runs of spaces and trims both ends.",
        "'-'.join(words) puts exactly one dash between words and none at the ends.",
    ],
    hints_ru=[
        "Сначала нижний регистр, потом пройди по символам: оставь ch, если ch.isalnum(), иначе пробел.",
        "str.split() без аргумента схлопывает серии пробелов и обрезает концы.",
        "'-'.join(words) ставит ровно один дефис между словами и ни одного по краям.",
    ],
    explanation_en=("The whole trick is split() without arguments: it does the trimming and the de-duplication of spaces "
                    "for you. Replacing instead of deleting symbols keeps 'Over-the-Hill' as three words."),
    explanation_ru=("Весь фокус – split() без аргументов: он сам обрезает края и схлопывает пробелы. Замена символов на "
                    "пробел вместо удаления сохраняет 'Over-the-Hill' как три слова."),
    talk_track=[
        "Say the trick is split() without arguments: trimming and repeats handled at once.",
        "Mention isalnum keeps Unicode letters too; ask whether ASCII-only slugs are wanted.",
    ],
    complexity="O(n)",
    followups=["How would you limit the slug to 50 characters without cutting a word?", "What about transliterating Cyrillic titles?"],
)

STARTER = '''
def slugify(title):
    ...
'''

EXAMPLES = [
    {"call": "slugify('Emerald Lake: 5 Tips!')", "expected": "'emerald-lake-5-tips'"},
    {"call": "slugify('  Hello   World ')", "expected": "'hello-world'"},
]

SOLUTION = '''
def slugify(title):
    chars = []
    for ch in title.lower():
        chars.append(ch if ch.isalnum() else " ")
    return "-".join("".join(chars).split())
'''

TESTS = '''
def test_title_with_symbols(ns, check):
    check(ns["slugify"]("Emerald Lake: 5 Tips!"), "emerald-lake-5-tips", "slugify('Emerald Lake: 5 Tips!')")

def test_spaces(ns, check):
    check(ns["slugify"]("  Hello   World "), "hello-world", "slugify('  Hello   World ')")

def test_dashes_become_words(ns, check):
    check(ns["slugify"]("Over-the-Hill mods!!!"), "over-the-hill-mods", "slugify('Over-the-Hill mods!!!')")

def test_empty_and_symbols(ns, check):
    check((ns["slugify"](""), ns["slugify"]("!!! ???")), ("", ""), "empty and symbols-only")

def test_unicode_letters(ns, check):
    check(ns["slugify"]("Шортс про Бали"), "шортс-про-бали", "slugify('Шортс про Бали')")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Lowercase, replace symbols with spaces, split, join: every step is the right one and the split() trick "
                 "is used knowingly. The character loop with a list and a second join is slightly more machinery than "
                 "the idea needs; a reviewer sees that you know the pieces but have not yet compressed them."),
        note_ru=("Нижний регистр, символы в пробелы, split, join: каждый шаг верный, и трюк со split() применён осознанно. "
                 "Цикл по символам со списком и вторым join – чуть больше механики, чем нужно идее; ревьюер видит, что "
                 "детали ты знаешь, но ещё не сжал их."),
    ),
    senior=dict(
        code='''
def slugify(title):
    """URL slug: lowercase words joined by single dashes, symbols dropped."""
    words = "".join(ch if ch.isalnum() else " " for ch in title.lower()).split()
    return "-".join(words)
''',
        note_en=("The same four steps in two lines, each line one idea: normalise into words, join with dashes. A senior "
                 "then talks about what the code does not decide yet: isalnum keeps Cyrillic and accents, so ask whether "
                 "the slug must be ASCII (unicodedata.normalize plus an encode is the next step) and whether a maximum "
                 "length applies. Those questions are the senior part; the code is just the start."),
        note_ru=("Те же четыре шага в двух строках, по одной идее на строку: нормализовать в слова, склеить дефисами. Дальше "
                 "сеньор говорит о том, чего код ещё не решает: isalnum оставляет кириллицу и акценты, так что спроси, нужен "
                 "ли slug только из ASCII (следующий шаг – unicodedata.normalize плюс encode) и есть ли предел длины. Эти "
                 "вопросы и есть сеньорская часть; код лишь начало."),
    ),
)
