META = dict(
    id="l0.comprehensions.best-and-worst", type="cloze", order=30,
    difficulty=1, minutes=3, world="tennis",
    concepts=["min-max-key", "sum", "lambda"],
    story_en="Which match was the marathon and which was over before the water break? And how many games in total, for the knees.",
    title="Best and worst",
    statement_en="Fill in the three built-ins: the match with the most games, the one with the fewest, and the total number of games.",
    hints_en=["max and min accept the same key= as sorted; sum adds up a generator expression directly."],
    hints_ru=["max и min принимают такой же key=, как sorted; sum складывает генераторное выражение напрямую."],
    explanation_en="max and min with a key return the whole element, not the key value, so you can index into it afterwards. sum over a generator never builds the intermediate list.",
    explanation_ru="max и min с ключом возвращают весь элемент, а не значение ключа, поэтому к нему можно обратиться дальше. sum по генератору не строит промежуточный список.",
)

STARTER = '''
matches = [{"opponent": "Ada", "games": 12}, {"opponent": "Byte", "games": 18}, {"opponent": "Cid", "games": 9}]
longest = ___(matches, key=lambda m: m["games"])["opponent"]    # "Byte"
shortest = ___(matches, key=lambda m: m["games"])["opponent"]   # "Cid"
total_games = ___(m["games"] for m in matches)                  # 39
'''

SOLUTION = '''
matches = [{"opponent": "Ada", "games": 12}, {"opponent": "Byte", "games": 18}, {"opponent": "Cid", "games": 9}]
longest = max(matches, key=lambda m: m["games"])["opponent"]
shortest = min(matches, key=lambda m: m["games"])["opponent"]
total_games = sum(m["games"] for m in matches)
'''

TESTS = '''
def test_longest(ns, check):
    check(ns["longest"], "Byte", "longest")

def test_shortest(ns, check):
    check(ns["shortest"], "Cid", "shortest")

def test_total(ns, check):
    check(ns["total_games"], 39, "total_games")
'''
