FAMILY = dict(
    id="gym.unpacking", order=7, tier=1,
    title_en="Unpacking instead of indexing", title_ru="Распаковка вместо индексов",
    rule_en="pair[0], pair[1] is name, score = pair. first = items[0]; rest = items[1:] is first, *rest = items. A swap is "
            "a, b = b, a. Pairs in a loop unpack in the for line: for name, score in pairs. A list passed as separate arguments is f(*items).",
    rule_ru="pair[0], pair[1] – это name, score = pair. first = items[0]; rest = items[1:] – это first, *rest = items. Обмен – "
            "a, b = b, a. Пары в цикле распаковываются в строке for: for name, score in pairs. Список как отдельные аргументы – f(*items).",
    phrase_en="I'll unpack the tuple so the parts get names instead of positions.",
    concepts=["tuple-unpacking", "star-args", "list-index"],
)
