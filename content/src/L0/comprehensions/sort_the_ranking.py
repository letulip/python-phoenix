META = dict(
    id="l0.comprehensions.sort-the-ranking", type="cloze", order=20,
    difficulty=1, minutes=2, world="tennis",
    concepts=["sorted-key", "lambda", "reverse-sort"],
    story_en="The academy ranking: highest rating first. Byte is on top and insists it is because of the hat.",
    title="Sort the ranking",
    statement_en="Fill in the blanks so the players are sorted by rating, highest first, and names come out as Byte, Pixel, Ada.",
    hints_en=["An inline function is written with the lambda keyword; descending order is reverse=True."],
    hints_ru=["Встроенная функция пишется через ключевое слово lambda; порядок по убыванию – reverse=True."],
    explanation_en="The key function tells sorted what to compare; it receives one tuple and returns the rating. reverse flips the order without touching the key.",
    explanation_ru="Функция key говорит sorted, что сравнивать; она получает один кортеж и возвращает рейтинг. reverse переворачивает порядок, не трогая ключ.",
)

STARTER = '''
players = [("Ada", 1200), ("Byte", 1450), ("Pixel", 1320)]
by_rating = sorted(players, key=___ p: p[1], reverse=___)
names = [name for name, rating in by_rating]
# names == ["Byte", "Pixel", "Ada"]
'''

SOLUTION = '''
players = [("Ada", 1200), ("Byte", 1450), ("Pixel", 1320)]
by_rating = sorted(players, key=lambda p: p[1], reverse=True)
names = [name for name, rating in by_rating]
'''

TESTS = '''
def test_names(ns, check):
    check(ns["names"], ["Byte", "Pixel", "Ada"], "names")

def test_top_player(ns, check):
    check(ns["by_rating"][0], ("Byte", 1450), "by_rating[0]")

def test_players_untouched(ns, check):
    check(ns["players"], [("Ada", 1200), ("Byte", 1450), ("Pixel", 1320)], "players unchanged")
'''
