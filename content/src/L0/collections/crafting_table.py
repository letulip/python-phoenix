META = dict(
    id="l0.collections.crafting-table", type="task", order=60,
    difficulty=2, minutes=7, world="game",
    concepts=["dict-basics", "dict-get", "in-operator", "truthiness"],
    story_en="Timmy wants to craft a torch: one stick, one coal. He has forty sticks and a deep sense of injustice.",
    title="Crafting table",
    statement_en=("Write craft(inventory, recipe) -> bool. Both are dicts of item -> count. If the inventory holds at least "
                  "the required count of every recipe item, subtract the counts from the inventory and return True. "
                  "Otherwise return False and leave the inventory exactly as it was. An empty recipe always succeeds."),
    hints_en=[
        "Two passes: first check every recipe item with inventory.get(item, 0) >= needed, only then subtract.",
        "If you subtract while checking, a failing recipe corrupts the inventory. Keep the loops separate.",
        "Return False inside the first loop as soon as one item is short; after the second loop return True.",
    ],
    hints_ru=[
        "Два прохода: сначала проверь каждый предмет рецепта через inventory.get(item, 0) >= needed, и только потом вычитай.",
        "Если вычитать во время проверки, неудачный рецепт испортит инвентарь. Держи циклы раздельно.",
        "Верни False прямо в первом цикле, как только чего-то не хватает; после второго цикла верни True.",
    ],
    explanation_en=("Check first, mutate second: that way a failed craft leaves no trace. dict.get(item, 0) treats a missing "
                    "item as zero, so a recipe asking for coal fails cleanly when there is no coal key at all."),
    explanation_ru=("Сначала проверка, потом изменение: тогда неудачный крафт не оставляет следов. dict.get(item, 0) считает "
                    "отсутствующий предмет нулём, поэтому рецепт с углём честно падает, даже если ключа coal нет вовсе."),
    talk_track=[
        "Say that the check and the mutation are separate passes, so failure leaves the inventory untouched.",
        "Mention dict.get(item, 0) handles missing items without KeyError.",
        "Complexity is O(k) in recipe items; inventory size does not matter.",
    ],
    complexity="O(k) in the number of recipe items",
    followups=["How would you return the list of missing items instead of False?", "Should craft mutate the inventory or return a new one?"],
)

STARTER = '''
def craft(inventory, recipe):
    ...
'''

EXAMPLES = [
    {"call": "craft({'stick': 2, 'coal': 1}, {'stick': 1, 'coal': 1})", "expected": "True"},
    {"call": "craft({'stick': 1}, {'stick': 1, 'coal': 1})", "expected": "False"},
]

SOLUTION = '''
def craft(inventory, recipe):
    for item, needed in recipe.items():
        if inventory.get(item, 0) < needed:
            return False
    for item, needed in recipe.items():
        inventory[item] -= needed
    return True
'''

TESTS = '''
def test_success_subtracts(ns, check):
    inv = {"stick": 2, "coal": 1}
    check(ns["craft"](inv, {"stick": 1, "coal": 1}), True, "craft returns True")
    check(inv, {"stick": 1, "coal": 0}, "inventory after a successful craft")

def test_missing_item_fails(ns, check):
    inv = {"stick": 1}
    check(ns["craft"](inv, {"stick": 1, "coal": 1}), False, "craft without coal")
    check(inv, {"stick": 1}, "inventory unchanged after failure")

def test_not_enough_fails(ns, check):
    inv = {"stick": 1}
    check(ns["craft"](inv, {"stick": 2}), False, "craft needing 2 sticks")
    check(inv, {"stick": 1}, "inventory unchanged")

def test_failure_leaves_no_trace(ns, check):
    inv = {"stick": 5, "coal": 0}
    check(ns["craft"](inv, {"stick": 1, "coal": 1}), False, "coal is zero")
    check(inv["stick"], 5, "sticks must not be spent when coal is missing")

def test_empty_recipe(ns, check):
    inv = {"stick": 1}
    check(ns["craft"](inv, {}), True, "empty recipe")
    check(inv, {"stick": 1}, "inventory unchanged by an empty recipe")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Two passes, check then mutate, and dict.get for missing items: the all-or-nothing rule holds and the "
                 "empty recipe works by construction. The reviewer's notes: the function changes its argument but returns "
                 "only a bool, so the caller never learns what was missing, and the invariant 'failure leaves no trace' "
                 "lives in your head rather than in a docstring."),
        note_ru=("Два прохода, сначала проверка, потом изменение, и dict.get для отсутствующих предметов: правило «всё или "
                 "ничего» держится, пустой рецепт работает сам собой. Заметки ревьюера: функция меняет аргумент, а "
                 "возвращает лишь bool, так что вызывающий не узнаёт, чего не хватило, а инвариант «неудача не оставляет "
                 "следов» живёт у тебя в голове, а не в докстринге."),
    ),
    senior=dict(
        code='''
def craft(inventory, recipe):
    """Consume `recipe` from `inventory`: all of it or nothing at all."""
    short = [item for item, needed in recipe.items() if inventory.get(item, 0) < needed]
    if short:
        return False
    for item, needed in recipe.items():
        inventory[item] -= needed
    return True
''',
        note_en=("Names the invariant in the docstring and computes the list of missing items instead of a flag: the "
                 "follow-up 'return what is missing' is now a one-line change. A senior also raises the design question "
                 "out loud: mutate the inventory or return a new one? The statement says mutate, so mutate, and say that "
                 "you noticed the choice."),
        note_ru=("Инвариант назван в докстринге, а вместо флага считается список недостающего: дополнительный вопрос "
                 "«верни, чего не хватает» теперь меняет одну строку. Сеньор ещё задаёт вопрос о дизайне вслух: менять "
                 "инвентарь или возвращать новый? Условие говорит менять, значит меняем, но говорим, что выбор заметили."),
    ),
)
