META = dict(
    id="l0.strings.palindrome-check", type="task", order=60,
    difficulty=2, minutes=6, world="everyday",
    concepts=["str-methods", "string-slicing", "str-case"],
    story_en="Pixel's favourite phrase is 'Taco cat'. Timmy says it is just a cat and a taco. The function decides.",
    title="Palindrome check",
    statement_en=("Write is_palindrome(text) -> bool: True when text reads the same forwards and backwards if you ignore "
                  "case and keep only letters and digits. An empty string counts as a palindrome."),
    hints_en=[
        "Normalise first: keep only characters where ch.isalnum() is True, lowercased, in a new string.",
        "Compare the cleaned string with its reverse: cleaned == cleaned[::-1].",
        "Build cleaned with a loop and +=, or with ''.join(ch.lower() for ch in text if ch.isalnum()).",
    ],
    hints_ru=[
        "Сначала нормализуй: оставь только символы, для которых ch.isalnum() истинно, в нижнем регистре, в новой строке.",
        "Сравни очищенную строку с её разворотом: cleaned == cleaned[::-1].",
        "Собери cleaned циклом с += или через ''.join(ch.lower() for ch in text if ch.isalnum()).",
    ],
    explanation_en=("Normalise, then compare: once punctuation and case are gone, the check is one line. The slice [::-1] "
                    "reverses any sequence. A two-pointer version avoids the extra copy but is more code."),
    explanation_ru=("Нормализуй, потом сравнивай: как только исчезли знаки препинания и регистр, проверка становится одной "
                    "строкой. Срез [::-1] разворачивает любую последовательность. Вариант с двумя указателями обходится "
                    "без копии, но кода больше."),
    talk_track=[
        "Say you normalise first so the comparison itself is one line.",
        "Mention the two-pointer alternative that avoids building a copy.",
        "Complexity: O(n) time, O(n) extra space for the cleaned copy.",
    ],
    complexity="O(n) time, O(n) space",
    followups=["Do it with two pointers and no extra string.", "Should accented or Cyrillic letters count? What does isalnum say?"],
)

STARTER = '''
def is_palindrome(text):
    ...
'''

EXAMPLES = [
    {"call": "is_palindrome('Taco cat')", "expected": "True"},
    {"call": "is_palindrome('hello')", "expected": "False"},
]

SOLUTION = '''
def is_palindrome(text):
    cleaned = ""
    for ch in text:
        if ch.isalnum():
            cleaned += ch.lower()
    return cleaned == cleaned[::-1]
'''

TESTS = '''
def test_taco_cat(ns, check):
    check(ns["is_palindrome"]("Taco cat"), True, "is_palindrome('Taco cat')")

def test_panama(ns, check):
    check(ns["is_palindrome"]("A man, a plan, a canal: Panama"), True, "the Panama sentence")

def test_hello(ns, check):
    check(ns["is_palindrome"]("hello"), False, "is_palindrome('hello')")

def test_empty(ns, check):
    check(ns["is_palindrome"](""), True, "is_palindrome('')")

def test_digits(ns, check):
    check(ns["is_palindrome"]("12321"), True, "is_palindrome('12321')")

def test_two_letters(ns, check):
    check(ns["is_palindrome"]("ab"), False, "is_palindrome('ab')")

def test_lemon(ns, check):
    check(ns["is_palindrome"]("No lemon, no melon"), True, "No lemon, no melon")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Normalise, then compare with the reversed slice: the shape is right and the empty string works for "
                 "free. Building cleaned with += in a loop is what most people write first; it is O(n) in practice "
                 "thanks to CPython's string trick, but a reviewer will still ask why not join, and 'I always do it "
                 "this way' is not the answer they want."),
        note_ru=("Нормализовать, потом сравнить с перевёрнутым срезом: форма верная, пустая строка работает даром. "
                 "Сборка cleaned через += в цикле – то, что большинство пишет первым; на практике это O(n) благодаря "
                 "трюку CPython, но ревьюер всё равно спросит, почему не join, и «я всегда так пишу» – не тот ответ, "
                 "которого он ждёт."),
    ),
    senior=dict(
        code='''
def is_palindrome(text):
    """True when `text` reads the same both ways, ignoring case and non-alphanumerics."""
    cleaned = "".join(ch.casefold() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]
''',
        note_en=("One expression for the normalisation, one for the check. casefold instead of lower is the senior tell: "
                 "it handles the German sharp s and friends that lower() leaves alone. A senior also names the "
                 "two-pointer version (O(1) extra space, no copy) and explains when it matters: streams or very long "
                 "inputs, not a sentence on a birthday card."),
        note_ru=("Одно выражение на нормализацию, одно на проверку. casefold вместо lower – сеньорская примета: он "
                 "справляется с немецким эсцетом и прочими случаями, которые lower() не трогает. Сеньор ещё назовёт версию "
                 "с двумя указателями (O(1) дополнительной памяти, без копии) и скажет, когда она важна: потоки или очень "
                 "длинные входы, а не фраза на поздравительной открытке."),
    ),
)
