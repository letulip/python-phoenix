META = dict(
    id="l0.collections.shelf-basics", type="retype", order=10,
    difficulty=1, minutes=3, world="game",
    concepts=["list-index", "slicing", "list-methods", "in-operator", "len"],
    story_en="Timmy's first shelf. He insists the compass goes last because 'it points to the end'.",
    title="First shelf",
    statement_en=("Retype the snippet exactly: indexing from both ends, a slice, append and remove, len and the in check. "
                  "Watch what the slice captures before the shelf changes."),
    hints_en=["shelf[-1] is the last item; shelf[1:3] takes positions 1 and 2; remove deletes by value, append adds to the end."],
    hints_ru=["shelf[-1] – последний элемент; shelf[1:3] берёт позиции 1 и 2; remove удаляет по значению, append добавляет в конец."],
    explanation_en=("middle was sliced before the list changed, so it still holds 'lamp'. A slice is a copy; the list "
                    "methods change the original in place and return None."),
    explanation_ru=("middle срезан до изменений, поэтому в нём остался 'lamp'. Срез – копия; методы списка меняют "
                    "оригинал на месте и возвращают None."),
)

MODEL = '''
shelf = ["rope", "lamp", "map", "compass"]
first, last = shelf[0], shelf[-1]
middle = shelf[1:3]
shelf.append("flag")
shelf.remove("lamp")
count = len(shelf)
has_map = "map" in shelf
'''

STARTER = ""

TESTS = '''
def test_ends(ns, check):
    check((ns["first"], ns["last"]), ("rope", "compass"), "first, last")

def test_middle_slice(ns, check):
    check(ns["middle"], ["lamp", "map"], "middle")

def test_shelf_after_changes(ns, check):
    check(ns["shelf"], ["rope", "map", "compass", "flag"], "shelf after append and remove")

def test_count_and_membership(ns, check):
    check((ns["count"], ns["has_map"]), (4, True), "count, has_map")
'''
