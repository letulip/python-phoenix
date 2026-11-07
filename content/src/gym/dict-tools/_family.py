FAMILY = dict(
    id="gym.dict-tools", order=6, tier=1,
    title_en="dict.get, setdefault and items", title_ru="dict.get, setdefault и items",
    rule_en="'if key in d: d[key] += 1 else: d[key] = 1' is d[key] = d.get(key, 0) + 1. 'if key in d: return d[key] else: "
            "return x' is d.get(key, x). Grouping is d.setdefault(key, []).append(item). Walk pairs with for key, value in d.items().",
    rule_ru="if key in d: d[key] += 1 else: d[key] = 1 – это d[key] = d.get(key, 0) + 1. if key in d: return d[key] else: "
            "return x – это d.get(key, x). Группировка – d.setdefault(key, []).append(item). По парам ходят через for key, value in d.items().",
    phrase_en="dict.get with a default covers the missing-key case in one call.",
    concepts=["dict-basics", "dict-get", "setdefault", "in-operator"],
)
