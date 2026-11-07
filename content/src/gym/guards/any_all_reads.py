META = dict(
    id="gym.guards.any-all-reads", type="predict", order=50,
    difficulty=1, minutes=1, world="tennis",
    concepts=["any-all", "ternary"],
    title="Read any, all and a conditional",
    statement_en="Write what this code prints, one line per print. Two booleans on a line are separated by a space.",
    hints_en=["any([]) is False and all([]) is True; the conditional expression picks one of the two words."],
    hints_ru=["any([]) – False, а all([]) – True; условное выражение выбирает одно из двух слов."],
    explanation_en="any and all are questions over a sequence and short-circuit like 'or' and 'and'. Their empty-input answers follow the same logic: no witness means any is False, no counter-example means all is True.",
    explanation_ru="any и all – вопросы к последовательности, и они замыкаются рано, как or и and. Ответы на пустой вход следуют той же логике: нет свидетеля – any даёт False, нет контрпримера – all даёт True.",
)

VARIANTS = [
    dict(SCORES="[180, 195, 172]", HI="190", LO="150"),
    dict(SCORES="[61, 48, 75]", HI="80", LO="50"),
    dict(SCORES="[10, 10]", HI="9", LO="10"),
]

SNIPPET = '''
scores = @SCORES@
print(any(s > @HI@ for s in scores), all(s > @LO@ for s in scores))
print(any([]), all([]))
print("hot" if max(scores) > @HI@ else "mild")
'''
