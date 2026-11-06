META = dict(
    id="l0.collections.rotate-shelf", type="task", order=66,
    difficulty=2, minutes=5, world="game",
    concepts=["slicing", "list-methods", "truthiness"],
    story_en="Timmy's hotbar has nine slots and one scroll wheel. Scroll past the end and the first slot comes back around. Scroll backwards and the game cries.",
    title="Rotate the shelf",
    statement_en=("Write rotate(shelf, k) -> list: a new list with the items moved k positions to the left, so "
                  "rotate(['a', 'b', 'c'], 1) is ['b', 'c', 'a']. k may be 0, larger than the length, or negative "
                  "(negative rotates to the right). The input list must not change and an empty shelf stays empty."),
    hints_en=[
        "An empty shelf has no length to divide by: return [] first.",
        "Reduce k with k % len(shelf); Python's modulo is never negative for a positive length, so -1 becomes len - 1.",
        "Two slices glued together do the move: shelf[k:] + shelf[:k].",
    ],
    hints_ru=[
        "У пустой полки нет длины, на которую можно делить: сначала верни [].",
        "Сведи k через k % len(shelf); остаток в Python не бывает отрицательным при положительной длине, так что -1 станет len - 1.",
        "Переезд делают два склеенных среза: shelf[k:] + shelf[:k].",
    ],
    explanation_en=("Rotation is two slices: the tail from k onwards, then the head before k. The modulo folds every k, "
                    "including negative ones, into the range 0..len-1, and slices always build a new list, so the input "
                    "stays as it was."),
    explanation_ru=("Поворот – это два среза: хвост от k и дальше, потом голова до k. Остаток сворачивает любое k, включая "
                    "отрицательное, в диапазон 0..len-1, а срезы всегда строят новый список, поэтому вход не меняется."),
    talk_track=[
        "Say the modulo normalises k, including negative values, and show -1 % 3 == 2.",
        "Point out that slicing copies, so the input is untouched by construction.",
        "Complexity O(n); mention collections.deque.rotate for a structure that rotates often.",
    ],
    complexity="O(n)",
    followups=["Rotate in place without creating a new list.", "What changes if shelf is a string instead of a list?"],
)

STARTER = '''
def rotate(shelf, k):
    ...
'''

EXAMPLES = [
    {"call": "rotate(['a', 'b', 'c'], 1)", "expected": "['b', 'c', 'a']"},
    {"call": "rotate(['a', 'b', 'c'], -1)", "expected": "['c', 'a', 'b']"},
]

SOLUTION = '''
def rotate(shelf, k):
    if not shelf:
        return []
    k = k % len(shelf)
    return shelf[k:] + shelf[:k]
'''

TESTS = '''
def test_left_by_one(ns, check):
    check(ns["rotate"](["a", "b", "c"], 1), ["b", "c", "a"], "rotate(['a', 'b', 'c'], 1)")

def test_right_by_one(ns, check):
    check(ns["rotate"](["a", "b", "c"], -1), ["c", "a", "b"], "rotate(['a', 'b', 'c'], -1)")

def test_k_larger_than_length(ns, check):
    check(ns["rotate"](["a", "b", "c"], 4), ["b", "c", "a"], "rotate by 4 equals rotate by 1")

def test_zero_and_full_turn(ns, check):
    check((ns["rotate"]([1, 2, 3], 0), ns["rotate"]([1, 2, 3], 3)), ([1, 2, 3], [1, 2, 3]), "k = 0 and k = len")

def test_empty(ns, check):
    check(ns["rotate"]([], 5), [], "rotate([], 5)")

def test_input_untouched(ns, check):
    shelf = ["a", "b", "c"]
    out = ns["rotate"](shelf, 2)
    check(shelf, ["a", "b", "c"], "input unchanged")
    check(out is shelf, False, "a new list is returned")
'''

LEVELS = dict(
    middle=dict(
        code='''
def rotate(shelf, k):
    result = list(shelf)
    if len(result) == 0:
        return result
    k = k % len(result)
    for _ in range(k):
        first = result.pop(0)
        result.append(first)
    return result
''',
        note_en=("Copies first, so the input is safe, and the modulo handles negative k: the instincts are right. The "
                 "engine is the problem: pop(0) shifts the whole list, so the loop is O(n * k), and an interviewer will "
                 "ask what happens with a million items and k close to n. The answer 'slices' is one line away."),
        note_ru=("Сначала копия, значит вход в безопасности, остаток обрабатывает отрицательное k: инстинкты верные. "
                 "Подводит движок: pop(0) сдвигает весь список, поэтому цикл – O(n * k), и интервьюер спросит, что будет "
                 "на миллионе элементов при k около n. Ответ «срезы» лежит в одной строке отсюда."),
    ),
    senior=dict(
        code='''
def rotate(shelf, k):
    """New list rotated k positions to the left (negative k rotates right)."""
    if not shelf:
        return []
    k %= len(shelf)          # -1 -> len - 1, len + 1 -> 1
    return shelf[k:] + shelf[:k]
''',
        note_en=("Two slices and a modulo: O(n), one pass, no mutation. The comment states the one non-obvious fact, that "
                 "Python's % never goes negative for a positive divisor, instead of leaving the reader to test it. A "
                 "senior adds that a structure rotated all the time wants collections.deque with rotate(), which is O(k), "
                 "and that the empty guard is there because len(shelf) would be a zero divisor."),
        note_ru=("Два среза и остаток: O(n), один проход, без мутаций. Комментарий фиксирует единственный неочевидный факт – "
                 "% в Python не уходит в минус при положительном делителе – вместо того чтобы оставить читателю проверять. "
                 "Сеньор добавит, что структура, которую крутят постоянно, просится в collections.deque с rotate() за O(k), "
                 "и что защита от пустого списка стоит потому, что len(shelf) был бы нулевым делителем."),
    ),
)
