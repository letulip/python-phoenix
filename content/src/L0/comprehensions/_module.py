MODULE = dict(
    id="l0.comprehensions", level=0, order=5,
    title_en="Comprehensions and sorting", title_ru="Включения и сортировка",
    concepts=["list-comprehension", "dict-comprehension", "set-comprehension", "comprehension-if",
              "sorted-key", "lambda", "reverse-sort", "min-max-key", "any-all", "sum"],
    diagnostic=["l0.comprehensions.leaderboard"],
    chapter_en="Act I · Chapter 5: The sorting machine", chapter_ru="Акт I · Глава 5: Сортировочная машина",
    story_en=("Coach Topspin storms in with a crate of match sheets from the tennis academy: ratings, rallies, serves. "
              "The studio's sorting machine can rank anything if you describe the result in one line. Pixel calls that "
              "line a comprehension and refuses to write loops for lists ever again."),
    story_ru=("Тренер Топспин врывается с ящиком протоколов из теннисной академии: рейтинги, розыгрыши, подачи. "
              "Сортировочная машина студии ранжирует что угодно, если описать результат одной строкой. Пиксель зовёт "
              "эту строку включением и отказывается впредь писать циклы для списков."),
    story_done_en="The leaderboard is sorted, the longest rally hangs framed on the wall and the machine idles. Only the lifeboats are left, and Dr. Candle is already pacing by the door with a crashing trading bot.",
    story_done_ru="Таблица лидеров отсортирована, самый длинный розыгрыш висит в рамке на стене, машина отдыхает. Остались только спасательные шлюпки, а у двери уже ходит доктор Кэндл с падающим торговым ботом.",
    card=dict(
        intro_en=("A comprehension builds a list, dict or set from an iterable in one expression: [f(x) for x in items if cond]. "
                  "Sorting takes a key function that says what to compare; min, max and sum accept the same key or a generator. "
                  "any and all answer yes/no questions over a whole collection."),
        intro_ru=("Включение строит список, словарь или множество из итерируемого одним выражением: [f(x) for x in items if cond]. "
                  "Сортировка принимает функцию key, которая говорит, что сравнивать; min, max и sum берут такой же key или "
                  "генератор. any и all отвечают да/нет по всей коллекции."),
        snippets=[
            dict(title_en="List, dict and set comprehensions", title_ru="Включения списка, словаря и множества",
                 code='scores = [61, 48, 75]\n[s * 2 for s in scores]             # [122, 96, 150]\n[s for s in scores if s >= 50]      # [61, 75]\n{s: s >= 50 for s in scores}        # {61: True, 48: False, 75: True}\n{s // 10 for s in scores}           # {4, 6, 7}\n',
                 note_en="Read it as 'for each s in scores, produce ...'. The if filters; the expression before for transforms.",
                 note_ru="Читай как «для каждого s из scores произвести ...». if фильтрует; выражение перед for преобразует."),
            dict(title_en="sorted with a key", title_ru="sorted с ключом",
                 code='players = [("Ada", 1200), ("Byte", 1450)]\nsorted(players, key=lambda p: p[1], reverse=True)   # Byte first\nsorted(words, key=len)                                # shortest first\nsorted(rows, key=lambda r: (-r["wins"], r["name"]))   # most wins, then name\n',
                 note_en="sorted returns a new list and is stable; negate numbers inside the key tuple to sort one field descending.",
                 note_ru="sorted возвращает новый список и устойчив; ставь минус перед числом в кортеже ключа, чтобы одно поле шло по убыванию."),
            dict(title_en="min, max, sum with keys and generators", title_ru="min, max, sum с ключами и генераторами",
                 code='longest = max(matches, key=lambda m: m["games"])\nshortest = min(matches, key=lambda m: m["games"])\ntotal = sum(m["games"] for m in matches)\nsum(1 for s in scores if s >= 50)                    # count the ones that qualify\n',
                 note_en="A generator expression inside sum, min or max avoids building a temporary list.",
                 note_ru="Генераторное выражение внутри sum, min или max обходится без временного списка."),
            dict(title_en="any and all", title_ru="any и all",
                 code='any(s > 190 for s in speeds)        # at least one\nall(s < 200 for s in speeds)        # every one\nall([])                             # True (nothing contradicts it)\n',
                 note_en="Both short-circuit: any stops at the first True, all at the first False.",
                 note_ru="Обе функции останавливаются досрочно: any на первом True, all на первом False."),
        ],
        gotchas_en=[
            "sorted(items) returns a new list; items.sort() sorts in place and returns None.",
            "A comprehension that needs an index or stacks three ifs should become a loop again.",
            "max() of an empty list raises ValueError; pass default=None when the list may be empty.",
        ],
        gotchas_ru=[
            "sorted(items) возвращает новый список; items.sort() сортирует на месте и возвращает None.",
            "Включение, которому нужен индекс или три вложенных if, лучше снова сделать циклом.",
            "max() от пустого списка бросает ValueError; передавай default=None, если список может быть пустым.",
        ],
        phrase_en="I'll sort with a key tuple so the tie-break is explicit.",
    ),
)
