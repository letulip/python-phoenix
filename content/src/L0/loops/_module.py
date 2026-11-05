MODULE = dict(
    id="l0.loops", level=0, order=3,
    title_en="Loops and conditions", title_ru="Циклы и условия",
    concepts=["for-loop", "while-loop", "range", "enumerate", "zip", "break-continue", "for-else",
              "ternary", "nested-loops", "accumulator"],
    diagnostic=["l0.loops.meow-purr"],
    chapter_en="Act I · Chapter 3: The conveyor belt", chapter_ru="Акт I · Глава 3: Конвейер",
    story_en=("The back room hides a conveyor belt that packs Captain Byte's orders. Pixel refuses to do anything twice "
              "by paw, so every repetitive job goes on the belt. Your task is to teach the belt to count, number things, "
              "pair them up and know when to stop."),
    story_ru=("В задней комнате прячется конвейер, который упаковывает заказы капитана Байта. Пиксель отказывается делать "
              "что-либо дважды лапами, поэтому всё повторяющееся отправляется на ленту. Твоя задача – научить ленту считать, "
              "нумеровать, складывать парами и вовремя останавливаться."),
    story_done_en="The belt hums in rhythm. Byte's duel schedule is printed, the Meow-Purr game is a hit, and Grandma Ada arrives with a broken signboard.",
    story_done_ru="Лента гудит в такт. Расписание дуэлей Байта напечатано, игра «Мяу-Мурр» имеет успех, а бабушка Ада уже пришла со сломанной вывеской.",
    card=dict(
        intro_en=("A loop repeats a block for each item, or while a condition holds. Python hands you the item itself, so "
                  "you rarely touch indexes; when you need numbers or pairs, enumerate and zip give them to you."),
        intro_ru=("Цикл повторяет блок для каждого элемента или пока выполняется условие. Python отдаёт сам элемент, поэтому "
                  "индексы нужны редко; когда нужны номера или пары, их выдают enumerate и zip."),
        snippets=[
            dict(title_en="for over items, with an accumulator", title_ru="for по элементам с накопителем",
                 code='total = 0\nfor coin in [5, 10, 25]:\n    total += coin           # 40\n\nfor n in range(3):          # 0, 1, 2\n    print(n)\nfor n in range(10, 0, -3):  # 10, 7, 4, 1\n    print(n)\n',
                 note_en="range(start, stop, step) never includes stop. The accumulator is created before the loop.",
                 note_ru="range(start, stop, step) никогда не включает stop. Накопитель создаётся до цикла."),
            dict(title_en="enumerate and zip", title_ru="enumerate и zip",
                 code='for i, name in enumerate(["Pixel", "Byte"], start=1):\n    print(f"{i}. {name}")        # 1. Pixel / 2. Byte\n\nfor name, price in zip(["rope", "lamp"], [3, 12]):\n    print(name, price)           # rope 3 / lamp 12\n',
                 note_en="enumerate yields (index, item); zip walks several lists in lockstep and stops at the shortest.",
                 note_ru="enumerate выдаёт (индекс, элемент); zip идёт по нескольким спискам в ногу и останавливается на самом коротком."),
            dict(title_en="while, break, continue", title_ru="while, break, continue",
                 code='n, steps = 20, 0\nwhile n > 1:\n    n //= 2\n    steps += 1              # 4 steps: 10, 5, 2, 1\n\nfor x in [3, -1, 4]:\n    if x < 0:\n        continue            # skip this item\n    if x > 3:\n        break               # leave the loop entirely\n',
                 note_en="A while loop needs something inside that moves toward the exit, or it runs forever (the stand kills it after 5 s).",
                 note_ru="Внутри while должно быть что-то, что ведёт к выходу, иначе цикл бесконечен (стенд убьёт его через 5 с)."),
            dict(title_en="for ... else and the one-line conditional", title_ru="for ... else и однострочное условие",
                 code='for name in crew:\n    if name not in allowed:\n        break\nelse:\n    print("everyone is allowed")   # only if no break happened\n\nlabel = "even" if n % 2 == 0 else "odd"\n',
                 note_en="The else of a loop means 'no break happened'. The conditional expression reads value-if-condition-else-value.",
                 note_ru="else у цикла означает «break не случился». Условное выражение читается как значение-если-условие-иначе-значение."),
            dict(title_en="Nested loops for pairs", title_ru="Вложенные циклы для пар",
                 code='names = ["a", "b", "c"]\nfor i in range(len(names)):\n    for j in range(i + 1, len(names)):\n        print(names[i], names[j])  # a b, a c, b c\n',
                 note_en="Start the inner index at i + 1 to get each unordered pair exactly once.",
                 note_ru="Начинай внутренний индекс с i + 1, чтобы получить каждую неупорядоченную пару ровно один раз."),
        ],
        gotchas_en=[
            "Changing a list while iterating over it skips elements: iterate over a copy (items[:]) or build a new list.",
            "range(5) is 0..4; off-by-one bugs live at the stop value.",
            "A while loop that makes no progress toward its exit never ends.",
        ],
        gotchas_ru=[
            "Изменение списка во время обхода пропускает элементы: обходи копию (items[:]) или собирай новый список.",
            "range(5) – это 0..4; ошибки на единицу живут у значения stop.",
            "while без продвижения к условию выхода не заканчивается никогда.",
        ],
        phrase_en="I'll use enumerate so I never manage the index by hand.",
    ),
)
