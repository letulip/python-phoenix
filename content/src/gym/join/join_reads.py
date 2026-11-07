META = dict(
    id="gym.join.join-reads", type="predict", order=30,
    difficulty=1, minutes=1, world="neutral",
    concepts=["split-join", "string-slicing"],
    title="Read four joins",
    statement_en="Write what this code prints, one line per print. Mind which string is the separator and which is the list.",
    hints_en=["The separator is the string before .join; the pieces come from the iterable inside the brackets."],
    hints_ru=["Разделитель – строка перед .join; куски берутся из итерируемого объекта в скобках."],
    explanation_en="join is called on the separator, not on the list. An empty separator glues pieces back to back, and a generator inside join is the normal way to transform the pieces on the way.",
    explanation_ru="join вызывается у разделителя, а не у списка. Пустой разделитель склеивает куски впритык, а генератор внутри join – обычный способ преобразовать куски по дороге.",
)

VARIANTS = [
    dict(PARTS="['ann', 'bob', 'cid']", NUMS="[1, 2, 3]"),
    dict(PARTS="['red', 'green', 'blue']", NUMS="[10, 20]"),
    dict(PARTS="['lake', 'sunrise']", NUMS="[7]"),
]

SNIPPET = '''
parts = @PARTS@
print("-".join(parts))
print(", ".join(parts[:2]))
print("".join(p[0] for p in parts))
print(" | ".join(str(n) for n in @NUMS@))
'''
