META = dict(
    id="l0.loops.duel-schedule", type="task", order=70,
    difficulty=2, minutes=6, world="game",
    concepts=["nested-loops", "range", "list-methods"],
    story_en="Captain Byte wants every crew member to duel every other exactly once. 'For morale,' he says.",
    title="Duel schedule",
    statement_en=("Write duels(crew) -> list[tuple[str, str]]: every unordered pair of crew members exactly once, each as "
                  "(earlier, later) in crew order, pairs sorted by the first member's position and then the second's. "
                  "A crew of one or none has no duels."),
    hints_en=[
        "Two loops: the outer picks index i, the inner picks j starting from i + 1.",
        "Append (crew[i], crew[j]); that order gives earlier-first automatically.",
        "Use range(len(crew)) for i and range(i + 1, len(crew)) for j.",
    ],
    hints_ru=[
        "Два цикла: внешний выбирает индекс i, внутренний – j, начиная с i + 1.",
        "Добавляй (crew[i], crew[j]); такой порядок сам даёт «раньше – первым».",
        "Для i используй range(len(crew)), для j – range(i + 1, len(crew)).",
    ],
    explanation_en=("Starting the inner loop at i + 1 skips self-duels and mirror pairs in one move. The number of pairs is "
                    "n*(n-1)/2, so O(n²) work is the size of the answer, not waste."),
    explanation_ru=("Старт внутреннего цикла с i + 1 одним ходом убирает дуэли с самим собой и зеркальные пары. Пар ровно "
                    "n*(n-1)/2, так что O(n²) – это размер ответа, а не расточительность."),
    talk_track=[
        "Explain why the inner loop starts at i + 1: no self-duels, no duplicates.",
        "State that the count is n*(n-1)/2, so O(n²) pairs is unavoidable.",
    ],
    complexity="O(n²), the size of the answer",
    followups=["How would itertools.combinations shorten this?", "What if some pairs refuse to duel each other?"],
)

STARTER = '''
def duels(crew):
    ...
'''

EXAMPLES = [
    {"call": "duels(['a', 'b', 'c'])", "expected": "[('a', 'b'), ('a', 'c'), ('b', 'c')]"},
    {"call": "duels(['solo'])", "expected": "[]"},
]

SOLUTION = '''
def duels(crew):
    pairs = []
    for i in range(len(crew)):
        for j in range(i + 1, len(crew)):
            pairs.append((crew[i], crew[j]))
    return pairs
'''

TESTS = '''
def test_three(ns, check):
    check(ns["duels"](["a", "b", "c"]), [("a", "b"), ("a", "c"), ("b", "c")], "duels(['a', 'b', 'c'])")

def test_solo_and_empty(ns, check):
    check((ns["duels"](["solo"]), ns["duels"]([])), ([], []), "duels for one and for none")

def test_five_gives_ten(ns, check):
    out = ns["duels"](["a", "b", "c", "d", "e"])
    check(len(out), 10, "5 crew -> 10 duels")
    check(len(set(out)), 10, "no duplicate pairs")

def test_no_self_duels(ns, check):
    out = ns["duels"](["x", "y", "z"])
    check(any(a == b for a, b in out), False, "nobody duels themselves")

def test_order(ns, check):
    check(ns["duels"](["Pixel", "Byte", "Ada"])[0], ("Pixel", "Byte"), "first duel")
'''
