META = dict(
    id="l0.loops.price-list", type="refactor", order=90,
    difficulty=2, minutes=6, world="everyday",
    concepts=["zip", "enumerate", "for-loop"],
    story_en="Grandma Ada's price list is printed by a loop that counts on its fingers. It has never been wrong. It has also never been read twice by anyone who stayed calm.",
    title="Price list without index arithmetic",
    statement_en=("price_list(names, prices) returns numbered 'n. name: price' lines and works, but it indexes two lists in "
                  "parallel through range(len(names)) and counts by hand. Rewrite it with zip to walk both lists together "
                  "and enumerate for the numbering from 1. No range(len(...)), no indexing and no manual counter may "
                  "remain. Behaviour must not change."),
    hints_en=[
        "zip(names, prices) yields (name, price) pairs; enumerate(..., start=1) numbers whatever you give it.",
        "Combine them: for number, (name, price) in enumerate(zip(names, prices), start=1).",
        "The f-string stays the same, only the names inside it change.",
    ],
    hints_ru=[
        "zip(names, prices) выдаёт пары (name, price); enumerate(..., start=1) нумерует всё, что ему дали.",
        "Соедини их: for number, (name, price) in enumerate(zip(names, prices), start=1).",
        "f-строка остаётся той же, меняются только имена внутри неё.",
    ],
    explanation_en=("zip pairs the lists by position, enumerate numbers the pairs, and start=1 replaces the hand-held "
                    "counter. The nested unpacking number, (name, price) is the standard shape for 'numbered pairs'; "
                    "the index variable disappears because nothing needs it any more."),
    explanation_ru=("zip соединяет списки по позициям, enumerate нумерует пары, а start=1 заменяет ручной счётчик. "
                    "Вложенная распаковка number, (name, price) – стандартная форма для «пронумерованных пар»; "
                    "переменная-индекс исчезает, потому что она больше никому не нужна."),
    talk_track=[
        "Say zip walks the lists together and enumerate numbers the result, so no index is left.",
        "Mention zip stops at the shorter list and that strict=True turns a mismatch into an error.",
    ],
    complexity="O(n)",
    followups=["What happens when names and prices differ in length? How would you make that loud?", "How would you format the price with two decimals?"],
)

STARTER = '''
def price_list(names, prices):
    lines = []
    number = 1
    for i in range(len(names)):
        lines.append(f"{number}. {names[i]}: {prices[i]}")
        number = number + 1
    return lines
'''

EXAMPLES = [
    {"call": "price_list(['rope', 'lamp'], [3, 12])", "expected": "['1. rope: 3', '2. lamp: 12']"},
]

SOLUTION = '''
def price_list(names, prices):
    lines = []
    for number, (name, price) in enumerate(zip(names, prices), start=1):
        lines.append(f"{number}. {name}: {price}")
    return lines
'''

TESTS = '''
def test_two_items(ns, check):
    check(ns["price_list"](["rope", "lamp"], [3, 12]), ["1. rope: 3", "2. lamp: 12"], "price_list(['rope', 'lamp'], [3, 12])")

def test_empty(ns, check):
    check(ns["price_list"]([], []), [], "price_list([], [])")

def test_three_items(ns, check):
    check(ns["price_list"](["a", "b", "c"], [1, 2, 3]), ["1. a: 1", "2. b: 2", "3. c: 3"], "three items numbered from 1")

def test_no_index_arithmetic(src, ast_tools, check):
    check(ast_tools.count_calls(src, "range"), 0, "no range(len(...)) left")
    check(ast_tools.count_nodes(src, "Subscript"), 0, "no names[i] indexing left")

def test_uses_zip_and_enumerate(src, ast_tools, check):
    check(ast_tools.uses_name(src, "zip"), True, "zip is used")
    check(ast_tools.uses_name(src, "enumerate"), True, "enumerate is used")

def test_no_manual_counter(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "AugAssign") + src.count("+ 1"), 0, "no hand-held counter left")
'''

LEVELS = dict(
    middle=dict(
        note_en=("zip pairs the lists, enumerate numbers the pairs, start=1 replaces the hand counter: this is the refactor "
                 "the task asked for and it is idiomatic. The nested unpacking is the one line a reviewer reads twice; that "
                 "is fine, it is the standard shape. What is still unsaid: what should happen when the lists differ in "
                 "length, because zip silently stops at the shorter one."),
        note_ru=("zip соединяет списки, enumerate нумерует пары, start=1 заменяет ручной счётчик: это тот рефакторинг, "
                 "который просило задание, и он идиоматичен. Вложенную распаковку ревьюер прочитает дважды; это нормально, "
                 "форма стандартная. Не сказано лишь одно: что делать, если списки разной длины, ведь zip молча "
                 "останавливается на более коротком."),
    ),
    senior=dict(
        code='''
def price_list(names, prices):
    """Numbered 'n. name: price' lines; names and prices must have the same length."""
    pairs = zip(names, prices, strict=True)
    return [f"{number}. {name}: {price}" for number, (name, price) in enumerate(pairs, start=1)]
''',
        note_en=("The comprehension states the output, and zip(strict=True) turns the silent truncation of mismatched lists "
                 "into a loud ValueError, which is what a price list wants: a missing price is a bug, not a shorter list. "
                 "A senior raises that before the interviewer asks 'what if the lists differ in length', and puts the "
                 "contract into the docstring."),
        note_ru=("Включение описывает результат, а zip(strict=True) превращает тихое усечение разных по длине списков в "
                 "громкий ValueError, чего прайс-лист и хочет: пропавшая цена – это баг, а не список покороче. Сеньор "
                 "поднимает это раньше, чем интервьюер спросит «а если списки разной длины», и записывает контракт в докстринг."),
    ),
)
