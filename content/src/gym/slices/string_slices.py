META = dict(
    id="gym.slices.string-slices", type="predict", order=18,
    difficulty=1, minutes=1, world="neutral",
    concepts=["string-slicing", "slicing"],
    title="Read four string slices",
    statement_en="Strings slice exactly like lists. Write what this code prints, one line per print.",
    hints_en=["word[0] and word[-1] are single characters; [:3] is the first three, [-3:] the last three, [::-1] the whole word backwards."],
    hints_ru=["word[0] и word[-1] – отдельные символы; [:3] – первые три, [-3:] – последние три, [::-1] – всё слово задом наперёд."],
    explanation_en="A string is a sequence, so every slice rule applies: half-open ranges, negative indexes from the end, a negative step for the reverse.",
    explanation_ru="Строка – последовательность, поэтому действуют все правила срезов: полуоткрытые диапазоны, отрицательные индексы с конца, отрицательный шаг для разворота.",
)

VARIANTS = [
    dict(WORD="phoenix"),
    dict(WORD="backpack"),
    dict(WORD="tennis"),
]

SNIPPET = '''
word = "@WORD@"
print(word[0], word[-1])
print(word[:3])
print(word[-3:])
print(word[::-1])
'''
