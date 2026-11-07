FAMILY = dict(
    id="gym.guards", order=8, tier=1,
    title_en="Guard clauses, any/all and conditional expressions", title_ru="Ранний return, any/all и условные выражения",
    rule_en="Handle the exceptions first and return; the main path then needs no nesting. A flag that a loop sets to True is "
            "any(cond for x in items), a flag set to False is all(...). 'if c: x = a else: x = b' is x = a if c else b.",
    rule_ru="Сначала обработай исключения из правила и выйди; основной путь тогда не нуждается во вложенности. Флаг, который цикл "
            "ставит в True, – это any(cond for x in items), флаг в False – all(...). if c: x = a else: x = b – это x = a if c else b.",
    phrase_en="I'll return early on the edge cases so the happy path reads top to bottom.",
    concepts=["early-return", "any-all", "ternary", "for-loop"],
)
