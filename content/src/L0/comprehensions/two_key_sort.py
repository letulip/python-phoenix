META = dict(
    id="l0.comprehensions.two-key-sort", type="cloze", order=50,
    difficulty=2, minutes=3, world="tennis",
    concepts=["sorted-key", "lambda"],
    story_en="Two players have two wins each. Points decide. Pixel says this is called a tie-break and looks very pleased.",
    title="Two-key sort",
    statement_en="Fill in the blanks so the table lists most wins first and, among equal wins, most points first: Byte, Cid, Ada.",
    hints_en=["sorted goes ascending; put a minus sign in front of a number inside the key tuple to make that field descending."],
    hints_ru=["sorted идёт по возрастанию; поставь минус перед числом внутри кортежа ключа, чтобы это поле шло по убыванию."],
    explanation_en="Tuples compare element by element, so a key tuple is a multi-level sort. Negating a number flips just that level while the rest stays ascending.",
    explanation_ru="Кортежи сравниваются поэлементно, поэтому кортеж-ключ – многоуровневая сортировка. Минус переворачивает только этот уровень, остальные идут по возрастанию.",
)

STARTER = '''
results = [("Ada", 2, 15), ("Byte", 3, 10), ("Cid", 2, 20)]   # name, wins, points
table = sorted(results, key=lambda r: (___r[1], ___r[2]))
# most wins first, then most points: Byte, Cid, Ada
'''

SOLUTION = '''
results = [("Ada", 2, 15), ("Byte", 3, 10), ("Cid", 2, 20)]
table = sorted(results, key=lambda r: (-r[1], -r[2]))
'''

TESTS = '''
def test_order(ns, check):
    check([r[0] for r in ns["table"]], ["Byte", "Cid", "Ada"], "table order")

def test_rows_intact(ns, check):
    check(ns["table"][1], ("Cid", 2, 20), "table[1]")
'''
