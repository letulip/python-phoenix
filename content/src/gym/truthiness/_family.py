FAMILY = dict(
    id="gym.truthiness", order=3, tier=1,
    title_en="Truthiness and is None", title_ru="Истинность и is None",
    rule_en="Empty containers, 0, '' and None are falsy: 'if not items' replaces len(items) == 0. Compare with None "
            "using 'is', never '=='. A function that answers True or False through an if/else returns the condition itself.",
    rule_ru="Пустые контейнеры, 0, '' и None ложны: if not items заменяет len(items) == 0. С None сравнивай через is, "
            "никогда через ==. Функция, которая отвечает True или False через if/else, возвращает само условие.",
    phrase_en="Empty is falsy, so I'll write 'if not items' and compare with None by identity.",
    concepts=["truthiness", "none-check", "ternary", "len"],
)
