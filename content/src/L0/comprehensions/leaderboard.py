META = dict(
    id="l0.comprehensions.leaderboard", type="task", order=60,
    difficulty=2, minutes=7, world="tennis",
    concepts=["sorted-key", "lambda", "reverse-sort", "list-comprehension"],
    story_en="Coach Topspin wants the top three on the clubhouse wall. Everybody with 1320 points wants to be listed before everybody else with 1320 points.",
    title="Leaderboard",
    statement_en=("Write leaderboard(ratings, top=3) -> list[str]. ratings is a dict of name -> rating. Return the names "
                  "ordered by rating descending; equal ratings are ordered by name ascending. Return at most top names."),
    hints_en=[
        "Sort ratings.items() with a key tuple: (-rating, name) gives descending rating and ascending name in one go.",
        "Slice the sorted list with [:top] before pulling out the names.",
        "A comprehension over the sliced pairs returns just the names.",
    ],
    hints_ru=[
        "Отсортируй ratings.items() с ключом-кортежем: (-rating, name) даёт рейтинг по убыванию и имя по возрастанию разом.",
        "Отрежь отсортированный список срезом [:top] до того, как вытащить имена.",
        "Включение по отрезанным парам возвращает только имена.",
    ],
    explanation_en=("The key tuple (-rating, name) encodes both rules: the minus flips the rating, the name breaks ties "
                    "alphabetically. Slicing with [:top] is safe when top is bigger than the list."),
    explanation_ru=("Кортеж-ключ (-rating, name) кодирует оба правила: минус переворачивает рейтинг, имя разрешает ничьи по "
                    "алфавиту. Срез [:top] безопасен, даже когда top больше длины списка."),
    talk_track=[
        "Explain the key tuple: negative rating for descending, name for the tie-break.",
        "Mention sorted is stable and O(n log n).",
        "Say slicing with [:top] is safe even when top exceeds the length.",
    ],
    complexity="O(n log n)",
    followups=["What if ratings can be None for unrated players?", "How would you give equal ratings the same rank number?"],
)

STARTER = '''
def leaderboard(ratings, top=3):
    ...
'''

EXAMPLES = [
    {"call": "leaderboard({'Ada': 1200, 'Byte': 1450, 'Pixel': 1320})", "expected": "['Byte', 'Pixel', 'Ada']"},
    {"call": "leaderboard({'a': 5, 'b': 5, 'c': 9}, top=2)", "expected": "['c', 'a']"},
]

SOLUTION = '''
def leaderboard(ratings, top=3):
    ordered = sorted(ratings.items(), key=lambda item: (-item[1], item[0]))
    return [name for name, rating in ordered[:top]]
'''

TESTS = '''
def test_basic(ns, check):
    check(ns["leaderboard"]({"Ada": 1200, "Byte": 1450, "Pixel": 1320}), ["Byte", "Pixel", "Ada"], "three players")

def test_tie_break_by_name(ns, check):
    check(ns["leaderboard"]({"zed": 10, "amy": 10, "bob": 12}), ["bob", "amy", "zed"], "ties ordered by name")

def test_top_limit(ns, check):
    check(ns["leaderboard"]({"a": 5, "b": 5, "c": 9}, top=2), ["c", "a"], "top=2")

def test_top_larger_than_size(ns, check):
    check(ns["leaderboard"]({"a": 1}, top=10), ["a"], "top larger than the board")

def test_empty(ns, check):
    check(ns["leaderboard"]({}), [], "empty ratings")

def test_top_zero(ns, check):
    check(ns["leaderboard"]({"a": 1}, top=0), [], "top=0")
'''
