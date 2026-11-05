MODULE = dict(
    id="l0.collections", level=0, order=2,
    title_en="Collections", title_ru="Коллекции",
    concepts=["list-index", "slicing", "list-methods", "tuple-unpacking", "dict-basics", "dict-get",
              "set-basics", "in-operator", "len", "truthiness", "none-check"],
    diagnostic=["l0.collections.crafting-table"],
    chapter_en="Act I · Chapter 2: The warehouse", chapter_ru="Акт I · Глава 2: Склад",
    story_en=("Behind the studio is a warehouse Pixel calls 'the collection'. Shelves are lists, labelled boxes are "
              "dicts, the no-duplicates bin is a set and the sealed crates are tuples. Timmy, a twelve-year-old regular "
              "with a very serious game inventory, has waited three years for someone to sort it."),
    story_ru=("За студией – склад, который Пиксель зовёт «коллекцией». Полки – списки, подписанные коробки – словари, "
              "корзина без дубликатов – множество, а запечатанные ящики – кортежи. Тимми, двенадцатилетний завсегдатай "
              "с очень серьёзным игровым инвентарём, три года ждёт, что кто-нибудь наведёт в нём порядок."),
    story_done_en="The warehouse is labelled, Timmy's inventory finally crafts a torch, and the conveyor belt in the back room starts to hum.",
    story_done_ru="Склад подписан, инвентарь Тимми наконец собирает факел, а в задней комнате загудел конвейер.",
    card=dict(
        intro_en=("Four containers cover most interview code: list (ordered, changeable), tuple (ordered, sealed), "
                  "dict (key to value) and set (unique members, fast 'in'). Pick by the question you will ask the data: "
                  "by position, by key, or 'is it there?'."),
        intro_ru=("Четыре контейнера закрывают почти весь код на интервью: list (упорядоченный, изменяемый), tuple "
                  "(упорядоченный, запечатанный), dict (ключ → значение) и set (уникальные элементы, быстрый in). "
                  "Выбирай по вопросу, который будешь задавать данным: по позиции, по ключу или «есть ли?»."),
        snippets=[
            dict(title_en="List: index, slice, change", title_ru="Список: индекс, срез, изменение",
                 code='shelf = ["rope", "lamp", "map"]\nshelf[0], shelf[-1]          # \'rope\', \'map\'\nshelf[1:3]                   # [\'lamp\', \'map\']  (end excluded)\nshelf.append("flag")\nshelf.remove("lamp")\nlen(shelf)                   # 3\n',
                 note_en="Negative indexes count from the end; a slice never raises, it just returns less.",
                 note_ru="Отрицательные индексы считают с конца; срез никогда не падает, он просто возвращает меньше."),
            dict(title_en="Dict: key to value", title_ru="Словарь: ключ → значение",
                 code='stock = {"potion": 3, "arrow": 20}\nstock["potion"]              # 3\nstock.get("shield", 0)       # 0 instead of KeyError\nstock["arrow"] -= 5\nfor item, count in stock.items():\n    print(item, count)\n',
                 note_en=".get with a default is the polite lookup; square brackets raise KeyError when the key is missing.",
                 note_ru=".get с умолчанием – вежливый поиск; квадратные скобки бросают KeyError, если ключа нет."),
            dict(title_en="Set: unique and fast", title_ru="Множество: уникально и быстро",
                 code='seen = set()\nseen.add("ann")\nseen.add("ann")\nlen(seen)                    # 1\n"ann" in seen                # True, fast even for millions\nset([1, 2, 2, 3])            # {1, 2, 3}\n',
                 note_en="Use a set for membership tests and de-duplication; it has no order you can rely on.",
                 note_ru="Множество – для проверок на вхождение и удаления дубликатов; на его порядок полагаться нельзя."),
            dict(title_en="Tuple and unpacking", title_ru="Кортеж и распаковка",
                 code='crate = ("gold", 12)\nkind, amount = crate\nfirst, *rest = [1, 2, 3]     # 1, [2, 3]\na, b = b, a                  # swap without a temp\n',
                 note_en="A tuple is a record you do not change; unpacking names its parts instead of indexing them.",
                 note_ru="Кортеж – запись, которую не меняют; распаковка даёт частям имена вместо индексов."),
            dict(title_en="Truthiness and None", title_ru="Истинность и None",
                 code='if not items:                # empty list, "", 0 and None are all falsy\n    return "nothing here"\nif note is None:             # compare with None using "is"\n    note = "no note"\n',
                 note_en="Empty containers are falsy, so 'if not items' is the idiom; compare to None with 'is', never '=='.",
                 note_ru="Пустые контейнеры ложны, поэтому идиома – if not items; с None сравнивай через is, а не =="),
        ],
        gotchas_en=[
            "shelf[1:3] ends before index 3, and shelf[5] raises IndexError while shelf[5:] is just empty.",
            "A dict keeps insertion order, a set does not: never rely on set order.",
            "A tuple with one element needs the comma: (5,) is a tuple, (5) is just 5.",
        ],
        gotchas_ru=[
            "shelf[1:3] заканчивается до индекса 3, а shelf[5] бросает IndexError, тогда как shelf[5:] просто пустой.",
            "Словарь хранит порядок вставки, множество – нет: на порядок множества не полагайся.",
            "Кортеж из одного элемента требует запятую: (5,) – кортеж, (5) – просто 5.",
        ],
        phrase_en="I'll keep these in a set, so membership checks are O(1).",
    ),
)
