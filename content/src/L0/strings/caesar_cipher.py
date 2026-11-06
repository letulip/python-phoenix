META = dict(
    id="l0.strings.caesar-cipher", type="task", order=80,
    difficulty=2, minutes=7, world="everyday",
    concepts=["ord-chr", "str-case", "str-methods"],
    story_en="Ada's recipe book, fully encrypted this time. Captain Byte wants the same function for his treasure notes. Everybody has secrets.",
    title="Caesar cipher",
    statement_en=("Write caesar(text, k) -> str: shift every Latin letter k positions along the alphabet, wrapping around and "
                  "keeping its case; every other character stays as it is. k may be negative or larger than 26."),
    hints_en=[
        "Pick the base per letter: ord('A') for uppercase, ord('a') for lowercase; non-letters are appended unchanged.",
        "(ord(ch) - base + k) % 26 + base wraps in both directions, even for negative k.",
        "Collect the pieces in a list and ''.join them at the end; it beats += on long texts.",
    ],
    hints_ru=[
        "Выбирай базу для каждой буквы: ord('A') для заглавных, ord('a') для строчных; не-буквы добавляй как есть.",
        "(ord(ch) - base + k) % 26 + base замыкает круг в обе стороны, даже при отрицательном k.",
        "Собирай куски в список и склей ''.join в конце; на длинных текстах это лучше, чем +=.",
    ],
    explanation_en=("Modulo arithmetic does all the wrapping: a shift of 27 equals a shift of 1, and -1 lands on z. "
                    "Keeping the base per character preserves case; checking isalpha and isascii leaves digits, spaces "
                    "and punctuation untouched."),
    explanation_ru=("Всё замыкание делает арифметика по модулю: сдвиг на 27 равен сдвигу на 1, а -1 приводит к z. База "
                    "для каждого символа сохраняет регистр; проверка isalpha и isascii оставляет цифры, пробелы и знаки "
                    "препинания нетронутыми."),
    talk_track=[
        "Say modulo handles both wrap-around and negative shifts.",
        "Mention you only shift ASCII letters, so punctuation and digits pass through.",
        "Complexity O(n); building a list and joining is linear, repeated += can be quadratic.",
    ],
    complexity="O(n)",
    followups=["How would you decrypt without knowing k?", "How would you support another alphabet?"],
)

STARTER = '''
def caesar(text, k):
    ...
'''

EXAMPLES = [
    {"call": "caesar('abc', 1)", "expected": "'bcd'"},
    {"call": "caesar('Hello, World!', 3)", "expected": "'Khoor, Zruog!'"},
]

SOLUTION = '''
def caesar(text, k):
    out = []
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)
'''

TESTS = '''
def test_simple(ns, check):
    check(ns["caesar"]("abc", 1), "bcd", "caesar('abc', 1)")

def test_sentence(ns, check):
    check(ns["caesar"]("Hello, World!", 3), "Khoor, Zruog!", "caesar('Hello, World!', 3)")

def test_wrap(ns, check):
    check(ns["caesar"]("xyz", 3), "abc", "caesar('xyz', 3)")

def test_round_trip(ns, check):
    check(ns["caesar"](ns["caesar"]("Pixel", 7), 19), "Pixel", "shift 7 then 19 returns the original")

def test_negative(ns, check):
    check(ns["caesar"]("ABC", -1), "ZAB", "caesar('ABC', -1)")

def test_large_shift(ns, check):
    check(ns["caesar"]("a b", 27), "b c", "caesar('a b', 27)")

def test_digits_untouched(ns, check):
    check(ns["caesar"]("r2d2", 1), "s2e2", "caesar('r2d2', 1)")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Per-character arithmetic with a base for each case and modulo 26: this is the textbook solution and it "
                 "handles negative and large shifts correctly. The list-plus-join is the right way to build the string. "
                 "What a reviewer adds: Python has a translation table built for exactly this, and knowing it changes "
                 "the loop into one call."),
        note_ru=("Арифметика по символам с базой для каждого регистра и остатком от 26: это решение из учебника, и "
                 "отрицательные и большие сдвиги оно обрабатывает верно. Список плюс join – правильный способ собрать "
                 "строку. Что добавит ревьюер: в Python есть таблица трансляции ровно для этого, и знание о ней "
                 "превращает цикл в один вызов."),
    ),
    senior=dict(
        code='''
import string

def caesar(text, k):
    """Shift ASCII letters by k, keeping case; everything else passes through."""
    k %= 26
    lower, upper = string.ascii_lowercase, string.ascii_uppercase
    table = str.maketrans(lower + upper, lower[k:] + lower[:k] + upper[k:] + upper[:k])
    return text.translate(table)
''',
        note_en=("Builds the shifted alphabet once and lets str.translate do the work in C: no per-character branching, "
                 "no ord/chr, and case handling falls out of the two alphabets. k %= 26 up front covers negative and "
                 "oversized shifts in one line. A senior notes the table could be cached per k and that the loop "
                 "version is what you write on a whiteboard when translate is not in your head."),
        note_ru=("Сдвинутый алфавит строится один раз, а работу делает str.translate на C: без ветвления по символам, без "
                 "ord/chr, а регистр получается сам из двух алфавитов. k %= 26 в начале одной строкой закрывает "
                 "отрицательные и большие сдвиги. Сеньор заметит, что таблицу можно кэшировать по k, а версия с циклом – "
                 "то, что пишут на доске, когда translate не вспомнился."),
    ),
)
