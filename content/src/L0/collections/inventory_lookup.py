META = dict(
    id="l0.collections.inventory-lookup", type="cloze", order=20,
    difficulty=1, minutes=2, world="game",
    concepts=["dict-basics", "dict-get"],
    story_en="Timmy has never owned a shield. The game should say zero, not crash.",
    title="Inventory lookup",
    statement_en=("Fill in the three blanks: read the potions by key, ask for shields with a default of 0 so that "
                  "no KeyError is raised and nothing is added, then spend 5 arrows in place."),
    hints_en=["Keys are strings in quotes. .get(key, default) never adds the key. Spending is -= on the existing entry."],
    hints_ru=["Ключи – строки в кавычках. .get(key, default) никогда не добавляет ключ. Потратить – это -= у существующей записи."],
    explanation_en="Square brackets demand that the key exists; .get is the question you ask when it might not. Augmented assignment updates the stored value in place.",
    explanation_ru="Квадратные скобки требуют, чтобы ключ существовал; .get – вопрос на случай, если его может не быть. Составное присваивание меняет сохранённое значение на месте.",
)

STARTER = '''
inventory = {"potion": 3, "arrow": 20}
potions = inventory[___]            # 3
shields = inventory.get(___, 0)     # 0, and no KeyError
inventory["arrow"] ___ 5            # 15 arrows left
'''

SOLUTION = '''
inventory = {"potion": 3, "arrow": 20}
potions = inventory["potion"]
shields = inventory.get("shield", 0)
inventory["arrow"] -= 5
'''

TESTS = '''
def test_potions(ns, check):
    check(ns["potions"], 3, "potions")

def test_shields_default(ns, check):
    check(ns["shields"], 0, "shields")

def test_arrows_spent(ns, check):
    check(ns["inventory"]["arrow"], 15, "inventory['arrow']")

def test_no_new_keys(ns, check):
    check(sorted(ns["inventory"]), ["arrow", "potion"], "inventory keys")
'''
