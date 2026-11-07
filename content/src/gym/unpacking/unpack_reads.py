META = dict(
    id="gym.unpacking.unpack-reads", type="predict", order=40,
    difficulty=1, minutes=1, world="neutral",
    concepts=["tuple-unpacking", "star-args"],
    title="Read three unpackings",
    statement_en="Write what this code prints, one line per print. The second line prints a value, a list and a value separated by spaces.",
    hints_en=["The swap happens before the first print; *middle collects a list, possibly empty; the loop unpacks each pair."],
    hints_ru=["Обмен происходит до первого print; *middle собирает список, возможно пустой; цикл распаковывает каждую пару."],
    explanation_en="Unpacking is positional: the first name takes the first item, the starred name takes the middle as a list, the last name the last item. print shows lists with brackets and strings without quotes.",
    explanation_ru="Распаковка позиционна: первое имя берёт первый элемент, имя со звёздочкой – середину списком, последнее имя – последний элемент. print показывает списки со скобками, а строки без кавычек.",
)

VARIANTS = [
    dict(A="1", B="2", ITEMS="[10, 20, 30, 40]", S1="7", S2="9"),
    dict(A="'ann'", B="'bob'", ITEMS="['x', 'y']", S1="3", S2="1"),
    dict(A="5", B="6", ITEMS="['a', 'b', 'c']", S1="0", S2="2"),
]

SNIPPET = '''
pair = (@A@, @B@)
x, y = pair
x, y = y, x
print(x, y)
first, *middle, last = @ITEMS@
print(first, middle, last)
for name, score in [("ann", @S1@), ("bob", @S2@)]:
    print(f"{name}={score}")
'''
