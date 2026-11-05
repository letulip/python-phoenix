META = dict(
    id="l0.strings.clean-the-order", type="retype", order=10,
    difficulty=1, minutes=3, world="everyday",
    concepts=["split-join", "strip", "str-case"],
    story_en="Grandma Ada's order slips arrive with random capitals and spaces. The oven does not care. The label printer does.",
    title="Clean the order",
    statement_en="Retype the snippet: split on commas, strip and lowercase every piece, then join with a separator and title-case the label.",
    hints_en=["Chain the methods: part.strip().lower(). join is called on the separator: ' | '.join(items)."],
    hints_ru=["Цепочка методов: part.strip().lower(). join вызывается у разделителя: ' | '.join(items)."],
    explanation_en="Normalising text is three verbs: split into pieces, strip the edges, unify the case. join is the inverse of split, and title() capitalises every word of the final label.",
    explanation_ru="Нормализация текста – три глагола: разрезать на куски, обрезать края, привести регистр. join обратен split, а title() делает заглавной первую букву каждого слова.",
)

MODEL = '''
raw = "  Cinnamon ROLL, sourdough , Rye bread "
items = []
for part in raw.split(","):
    items.append(part.strip().lower())
label = " | ".join(items).title()
'''

STARTER = ""

TESTS = '''
def test_items(ns, check):
    check(ns["items"], ["cinnamon roll", "sourdough", "rye bread"], "items")

def test_label(ns, check):
    check(ns["label"], "Cinnamon Roll | Sourdough | Rye Bread", "label")
'''
