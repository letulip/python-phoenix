FAMILY = dict(
    id="gym.comprehensions", order=5, tier=1,
    title_en="Comprehensions instead of append loops", title_ru="Включения вместо циклов с append",
    rule_en="A loop that only appends is a comprehension: [f(x) for x in items if cond]. A loop that only adds up is "
            "sum(...) over a generator, a loop that only builds a dict is {k: v for ...}. Keep the loop when it does more than one thing.",
    rule_ru="Цикл, который только делает append, – это включение: [f(x) for x in items if cond]. Цикл, который только "
            "складывает, – sum(...) по генератору; цикл, который только строит словарь, – {k: v for ...}. Цикл остаётся, когда он делает больше одного дела.",
    phrase_en="That loop only collects, so I'll write it as a comprehension.",
    concepts=["list-comprehension", "dict-comprehension", "comprehension-if", "sum", "any-all", "str-methods"],
)
