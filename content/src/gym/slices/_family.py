FAMILY = dict(
    id="gym.slices", order=1, tier=1,
    title_en="Slices and negative indexes", title_ru="Срезы и отрицательные индексы",
    rule_en="items[len(items) - 1] is items[-1]. A loop over range(len(items) - 1) that collects items[i] is items[:-1]. "
            "items[::-1] reverses, items[-n:] is the tail, items[a:b] never raises.",
    rule_ru="items[len(items) - 1] – это items[-1]. Цикл по range(len(items) - 1), который собирает items[i], – это items[:-1]. "
            "items[::-1] разворачивает, items[-n:] – хвост, items[a:b] никогда не падает.",
    phrase_en="I'll slice instead of indexing by hand.",
    concepts=["slicing", "list-index", "string-slicing"],
)
