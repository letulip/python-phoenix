FAMILY = dict(
    id="gym.enumerate-zip", order=4, tier=1,
    title_en="enumerate and zip instead of range(len())", title_ru="enumerate и zip вместо range(len())",
    rule_en="for i in range(len(items)) that only reads items[i] is for item in items. When the position is needed too, "
            "enumerate(items, start=1). Two lists walked side by side are zip(a, b). A counter you bump by hand means enumerate is missing.",
    rule_ru="for i in range(len(items)), который только читает items[i], – это for item in items. Когда нужна и позиция – "
            "enumerate(items, start=1). Два списка, которые идут рядом, – zip(a, b). Счётчик, который ты увеличиваешь руками, значит, что не хватает enumerate.",
    phrase_en="I'll let enumerate and zip carry the indexes for me.",
    concepts=["enumerate", "zip", "range", "for-loop", "sum"],
)
