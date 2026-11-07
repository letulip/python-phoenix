META = dict(
    id="gym.slices.slice-reads", type="predict", order=20,
    difficulty=1, minutes=2, world="neutral",
    concepts=["slicing", "list-index"],
    title="Read three slices",
    statement_en="Write exactly what this code prints, one line per print. Lists print with square brackets and single quotes around strings.",
    hints_en=["start:stop:step – the stop index is excluded, a negative start counts from the end, a negative step walks backwards."],
    hints_ru=["start:stop:step – индекс stop не включается, отрицательный start считает с конца, отрицательный шаг идёт назад."],
    explanation_en="Slices are half-open: [1:3] takes indexes 1 and 2. [-2:] is 'from the second-to-last to the end'. [::-1] is the reversed copy.",
    explanation_ru="Срезы полуоткрыты: [1:3] берёт индексы 1 и 2. [-2:] – «со второго с конца до конца». [::-1] – перевёрнутая копия.",
)

VARIANTS = [
    dict(ITEMS="['a', 'b', 'c', 'd', 'e']"),
    dict(ITEMS="[10, 20, 30, 40, 50, 60]"),
    dict(ITEMS="['sun', 'rain', 'wind', 'snow']"),
]

SNIPPET = '''
items = @ITEMS@
print(items[1:3])
print(items[-2:])
print(items[::-1])
'''
