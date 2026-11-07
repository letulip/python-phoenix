FAMILY = dict(
    id="gym.join", order=2, tier=1,
    title_en="join instead of +=", title_ru="join вместо +=",
    rule_en="A string built with += in a loop is a list of pieces plus ', '.join(pieces). join puts the separator "
            "between the items, so there is nothing to trim at the end, and it takes any iterable, a generator included.",
    rule_ru="Строка, собранная через += в цикле, – это список кусков плюс ', '.join(pieces). join ставит разделитель "
            "между элементами, поэтому в конце нечего отрезать, и принимает любой итерируемый объект, включая генератор.",
    phrase_en="I'll collect the parts and join them once.",
    concepts=["split-join", "f-string", "str-methods", "for-loop", "enumerate"],
)
