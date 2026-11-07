META = dict(
    id="gym.slices.tail-and-middle", type="cloze", order=16,
    difficulty=1, minutes=1, world="tennis",
    concepts=["slicing"],
    title="Tail, head and middle",
    statement_en="Fill in the three slices: the last three scores, the first two, and everything except the first and the last. Each blank is the part inside the square brackets.",
    hints_en=["A negative start counts from the end ([-3:]), a stop alone cuts the head ([:2]), and [1:-1] drops one item at each end."],
    hints_ru=["Отрицательный start считает с конца ([-3:]), один stop отрезает голову ([:2]), а [1:-1] убирает по элементу с каждого края."],
    explanation_en="Three shapes cover most slicing: [-n:] for the tail, [:n] for the head, [a:-b] for the middle. None of them raises when the list is short; they just return less.",
    explanation_ru="Три формы закрывают почти все срезы: [-n:] для хвоста, [:n] для головы, [a:-b] для середины. Ни одна не падает на коротком списке, они просто возвращают меньше.",
)

VARIANTS = [
    dict(SCORES="[10, 25, 7, 31, 18, 22]", LAST3="[31, 18, 22]", FIRST2="[10, 25]", MIDDLE="[25, 7, 31, 18]"),
    dict(SCORES="[3, 1, 4, 1, 5, 9, 2]", LAST3="[5, 9, 2]", FIRST2="[3, 1]", MIDDLE="[1, 4, 1, 5, 9]"),
    dict(SCORES="[60, 64, 76, 70, 62]", LAST3="[76, 70, 62]", FIRST2="[60, 64]", MIDDLE="[64, 76, 70]"),
]

STARTER = '''
scores = @SCORES@
last_three = scores[___]      # @LAST3@
first_two = scores[___]       # @FIRST2@
middle = scores[___]          # @MIDDLE@  (everything except the first and the last)
'''

SOLUTION = '''
scores = @SCORES@
last_three = scores[-3:]
first_two = scores[:2]
middle = scores[1:-1]
'''

TESTS = '''
def test_last_three(ns, check):
    check(ns["last_three"], @LAST3@, "last_three")

def test_first_two(ns, check):
    check(ns["first_two"], @FIRST2@, "first_two")

def test_middle(ns, check):
    check(ns["middle"], @MIDDLE@, "middle")

def test_scores_untouched(ns, check):
    check(ns["scores"], @SCORES@, "scores unchanged")
'''
