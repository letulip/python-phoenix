META = dict(
    id="l0.collections.roll-call", type="task", order=70,
    difficulty=1, minutes=5, world="game",
    concepts=["in-operator", "list-methods", "set-basics"],
    story_en="Captain Byte's roll call. The parrot used to do this too. The parrot had a better memory than the first mate.",
    title="Roll call",
    statement_en=("Write missing(crew, present) -> list. crew is the list of names in boarding order; present is a list or set "
                  "of names who showed up. Return the names that did not show up, in crew order. Names in present that are "
                  "not in crew are ignored."),
    hints_en=[
        "Walk the crew in order and collect the names that are not in present.",
        "Turn present into a set first, set(present), so the 'in' check is fast and works for lists too.",
    ],
    hints_ru=[
        "Пройди по crew по порядку и собери имена, которых нет в present.",
        "Сначала преврати present в множество, set(present), чтобы проверка in была быстрой и работала и для списков.",
    ],
    explanation_en=("Order comes from crew, so crew is what you iterate. Converting present to a set makes each membership "
                    "check O(1), which matters once the crew is a thousand pirates long."),
    explanation_ru=("Порядок задаёт crew, поэтому обходим именно его. Превращение present в множество делает каждую проверку "
                    "O(1), что важно, когда команда – тысяча пиратов."),
    talk_track=[
        "State that the order must come from crew, so you iterate crew, not present.",
        "Mention converting present to a set makes each check O(1).",
    ],
    complexity="O(n + m) for n crew and m present",
    followups=["What if names can repeat in crew?", "How would you also report who is present but not in the crew?"],
)

STARTER = '''
def missing(crew, present):
    ...
'''

EXAMPLES = [
    {"call": "missing(['Pixel', 'Byte', 'Ada'], {'Byte'})", "expected": "['Pixel', 'Ada']"},
    {"call": "missing(['Pixel'], ['Pixel'])", "expected": "[]"},
]

SOLUTION = '''
def missing(crew, present):
    here = set(present)
    absent = []
    for name in crew:
        if name not in here:
            absent.append(name)
    return absent
'''

TESTS = '''
def test_basic(ns, check):
    check(ns["missing"](["Pixel", "Byte", "Ada"], {"Byte"}), ["Pixel", "Ada"], "missing(['Pixel', 'Byte', 'Ada'], {'Byte'})")

def test_everyone_here(ns, check):
    check(ns["missing"](["Pixel", "Byte"], ["Byte", "Pixel"]), [], "all present")

def test_nobody_here(ns, check):
    check(ns["missing"](["Pixel", "Byte"], []), ["Pixel", "Byte"], "nobody present")

def test_strangers_ignored(ns, check):
    check(ns["missing"](["Pixel"], {"Ghost", "Pixel"}), [], "strangers in present are ignored")

def test_order_is_crew_order(ns, check):
    check(ns["missing"](["c", "a", "b"], {"a"}), ["c", "b"], "crew order kept")

def test_empty_crew(ns, check):
    check(ns["missing"]([], {"x"}), [], "empty crew")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Converts present to a set once and walks the crew in order: the right data structure and the right "
                 "loop, so the complexity is already O(n + m). It is still a four-line accumulator for a one-line idea; "
                 "nothing wrong with that, it just stops one step before the idiom."),
        note_ru=("present превращён в множество один раз, а обход идёт по crew по порядку: верная структура данных и "
                 "верный цикл, сложность уже O(n + m). Но это четырёхстрочный накопитель для идеи в одну строку; "
                 "ошибки нет, просто остановка за шаг до идиомы."),
    ),
    senior=dict(
        code='''
def missing(crew, present):
    """Crew members absent from `present`, in crew order."""
    here = set(present)
    return [name for name in crew if name not in here]
''',
        note_en=("The comprehension states the result: crew members not in the set. Building the set once outside the "
                 "comprehension keeps it O(n + m); writing 'name not in present' on a list would be O(n * m), and a senior "
                 "names that trap without being asked. Duplicates in crew stay duplicates, which the docstring states if "
                 "the interviewer cares."),
        note_ru=("Включение описывает результат: члены команды, которых нет в множестве. Множество построено один раз "
                 "снаружи включения, поэтому остаётся O(n + m); «name not in present» по списку дало бы O(n * m), и сеньор "
                 "называет эту ловушку без вопроса. Дубликаты в crew остаются дубликатами, и докстринг это скажет, если "
                 "интервьюеру важно."),
    ),
)
