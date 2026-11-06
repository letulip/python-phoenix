META = dict(
    id="l0.strings.censor", type="task", order=65,
    difficulty=2, minutes=6, world="game",
    concepts=["split-join", "str-case", "str-methods"],
    story_en="Timmy's game chat has a word filter. It replaces rude words with asterisks and, according to Timmy, 'ruins everything'. Pixel approves of the filter.",
    title="Chat filter",
    statement_en=("Write censor(text, banned) -> str. text is words separated by single spaces; banned is a set of "
                  "lowercase words. Replace every word whose lowercase form is in banned with asterisks of the same "
                  "length, keep every other word as it is, and join the words back with single spaces. An empty text "
                  "returns ''."),
    hints_en=[
        "text.split(' ') gives the words; compare word.lower() with the banned set.",
        "A banned word becomes '*' * len(word); an allowed word stays as it was.",
        "Collect the results in a list and ' '.join them.",
    ],
    hints_ru=[
        "text.split(' ') даёт слова; сравнивай word.lower() с множеством banned.",
        "Запрещённое слово становится '*' * len(word); разрешённое остаётся как было.",
        "Собери результаты в список и склей через ' '.join.",
    ],
    explanation_en=("split, decide per word, join: the standard shape for 'transform some words'. Lowercasing only the "
                    "comparison keeps the original spelling of the allowed words, and '*' * len(word) keeps the line "
                    "the same width, so the message still looks like a message."),
    explanation_ru=("split, решение по каждому слову, join: стандартная форма для «преобразовать некоторые слова». "
                    "Нижний регистр только для сравнения сохраняет исходное написание разрешённых слов, а '*' * len(word) "
                    "сохраняет ширину строки, так что сообщение по-прежнему выглядит как сообщение."),
    talk_track=[
        "Say you split, decide per word, and join: the transformation never touches the original string.",
        "Mention the comparison is lowercased but the output keeps the original case of allowed words.",
        "Complexity O(n) with a set for banned; a list would make it O(n * m).",
    ],
    complexity="O(n) with a set of banned words",
    followups=["What about 'noob!' with punctuation attached?", "How would you censor 'n00b' spelled with zeros?"],
)

STARTER = '''
def censor(text, banned):
    ...
'''

EXAMPLES = [
    {"call": "censor('you NOOB lol', {'noob'})", "expected": "'you **** lol'"},
    {"call": "censor('gg everyone', {'noob'})", "expected": "'gg everyone'"},
]

SOLUTION = '''
def censor(text, banned):
    words = []
    for word in text.split(" "):
        if word.lower() in banned:
            words.append("*" * len(word))
        else:
            words.append(word)
    return " ".join(words)
'''

TESTS = '''
def test_one_banned_word(ns, check):
    check(ns["censor"]("you NOOB lol", {"noob"}), "you **** lol", "censor('you NOOB lol', {'noob'})")

def test_nothing_banned(ns, check):
    check(ns["censor"]("gg everyone", {"noob"}), "gg everyone", "censor('gg everyone', {'noob'})")

def test_several(ns, check):
    check(ns["censor"]("noob says Noob", {"noob", "says"}), "**** **** ****", "every banned word, any case")

def test_empty_text(ns, check):
    check(ns["censor"]("", {"noob"}), "", "censor('', ...)")

def test_keeps_case_of_allowed_words(ns, check):
    check(ns["censor"]("GG Pixel", {"noob"}), "GG Pixel", "allowed words keep their case")

def test_length_preserved(ns, check):
    check(len(ns["censor"]("a verylongword b", {"verylongword"})), len("a verylongword b"), "asterisks keep the width")
'''

LEVELS = dict(
    middle=dict(
        code='''
def censor(text, banned):
    result = ""
    for word in text.split(" "):
        if word.lower() in banned:
            result = result + "*" * len(word) + " "
        else:
            result = result + word + " "
    return result.strip()
''',
        note_en=("Passes the tests, and that is the problem: it passes by accident. The trailing space is added every time "
                 "and removed with strip(), which would also eat spaces that belong to the message. Building a string "
                 "with + in a loop is the habit reviewers notice first; the fix is the list-and-join shape."),
        note_ru=("Тесты проходит, и в этом проблема: проходит случайно. Хвостовой пробел добавляется каждый раз и снимается "
                 "через strip(), который съел бы и пробелы, принадлежащие сообщению. Сборка строки через + в цикле – "
                 "привычка, которую ревьюеры замечают первой; лекарство – форма «список и join»."),
    ),
    senior=dict(
        code='''
def censor(text, banned):
    """Replace banned words (case-insensitive) with asterisks of the same length."""
    return " ".join("*" * len(word) if word.casefold() in banned else word for word in text.split(" "))
''',
        note_en=("One join over a generator with a conditional expression: the whole rule in a line that still reads "
                 "left to right. casefold is the correct case-insensitive comparison, not lower. A senior then says what "
                 "the function does not handle, punctuation glued to words and leetspeak, and asks whether banned "
                 "arrives lowercase or should be normalised at the boundary, before writing a single extra line."),
        note_ru=("Один join по генератору с условным выражением: всё правило в одной строке, которая читается слева направо. "
                 "casefold – корректное сравнение без учёта регистра, а не lower. Дальше сеньор говорит, чего функция не "
                 "делает: знаки препинания, приклеенные к словам, и leetspeak, и спрашивает, приходит ли banned в нижнем "
                 "регистре или его нормализовать на границе, прежде чем писать хоть одну лишнюю строку."),
    ),
)
