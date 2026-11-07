META = dict(
    id="gym.truthiness.truthy-reads", type="predict", order=40,
    difficulty=1, minutes=1, world="neutral",
    concepts=["truthiness"],
    title="Truthy or falsy?",
    statement_en="For each value the loop prints its repr and the word truthy or falsy. Write the output, one line per value.",
    hints_en=["Falsy: None, 0, 0.0, '', empty list/dict/tuple/set. Everything else is truthy, including '0', ' ' and [0]."],
    hints_ru=["Ложные: None, 0, 0.0, '', пустые список/словарь/кортеж/множество. Всё остальное истинно, включая '0', ' ' и [0]."],
    explanation_en="Truthiness is about emptiness and zero, not about meaning: the string '0' is a non-empty string, the list [0] has one item. That is why 'if not x' is a question about containers, not about contents.",
    explanation_ru="Истинность – про пустоту и ноль, а не про смысл: строка '0' – непустая строка, список [0] – из одного элемента. Поэтому if not x – вопрос о контейнере, а не о содержимом.",
)

VARIANTS = [
    dict(VALUES="0, '0', [], [0], None, '', ' '"),
    dict(VALUES="0.0, 'False', {}, {'a': 1}, (), (0,), -1"),
    dict(VALUES="'', 'none', [], [[]], 1, 0, 'x'"),
]

SNIPPET = '''
values = [@VALUES@]
for v in values:
    print(repr(v), "truthy" if v else "falsy")
'''
