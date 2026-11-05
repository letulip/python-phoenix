MODULE = dict(
    id="l0.strings", level=0, order=4,
    title_en="Strings", title_ru="Строки",
    concepts=["split-join", "strip", "replace", "find-in", "f-string", "format-spec", "str-methods",
              "str-case", "ord-chr", "string-slicing"],
    diagnostic=["l0.strings.palindrome-check"],
    chapter_en="Act I · Chapter 4: The signboard", chapter_ru="Акт I · Глава 4: Вывеска",
    story_en=("Grandma Ada runs the harbour bakery, and her signboard has been shouting in CAPITALS since the storm. "
              "She wants clean labels, honest price tags and, for reasons she will not explain, a secret code for the "
              "recipe book. Text work is studio work."),
    story_ru=("Бабушка Ада держит пекарню в гавани, и её вывеска со времён шторма кричит КАПСОМ. Ей нужны чистые ярлыки, "
              "честные ценники и, по причинам, которые она не объясняет, секретный шифр для книги рецептов. "
              "Работа с текстом – работа студии."),
    story_done_en="The signboard reads 'Ada's Bakery' in a calm font, the price tags line up to the cent and the recipe book is encrypted. Ada pays in cinnamon rolls; Coach Topspin is next in line.",
    story_done_ru="Вывеска спокойным шрифтом читает «Ada's Bakery», ценники выровнены до цента, книга рецептов зашифрована. Ада платит булочками с корицей; следующий в очереди – тренер Топспин.",
    card=dict(
        intro_en=("Strings are immutable sequences of characters: every method returns a new string. Most interview text "
                  "work is split, strip, join, replace, case changes, slicing and f-strings; ord and chr turn letters into "
                  "numbers and back."),
        intro_ru=("Строки – неизменяемые последовательности символов: каждый метод возвращает новую строку. Почти вся "
                  "работа с текстом на интервью – split, strip, join, replace, смена регистра, срезы и f-строки; "
                  "ord и chr превращают буквы в числа и обратно."),
        snippets=[
            dict(title_en="split, strip, join", title_ru="split, strip, join",
                 code='raw = "  rye, sourdough ,bagel "\nparts = raw.split(",")              # [\'  rye\', \' sourdough \', \'bagel \']\nclean = [p.strip() for p in parts]  # [\'rye\', \'sourdough\', \'bagel\']\n" | ".join(clean)                   # \'rye | sourdough | bagel\'\n"a b  c".split()                    # [\'a\', \'b\', \'c\']  (any whitespace)\n',
                 note_en="join is a method of the separator string. split() with no argument splits on any whitespace and drops empty pieces.",
                 note_ru="join – метод строки-разделителя. split() без аргумента режет по любым пробелам и выбрасывает пустые куски."),
            dict(title_en="Case, replace, search", title_ru="Регистр, замена, поиск",
                 code='sign = "Ada\'s Bakery: fresh bread"\nsign.upper(), sign.lower(), sign.title()\nsign.replace("bread", "rolls")\n"bread" in sign                     # True\nsign.find("fresh")                  # 14, or -1 when missing\nsign.startswith("Ada"), sign.endswith("!")\n',
                 note_en="'in' answers yes or no; find gives a position and -1 instead of raising, unlike index.",
                 note_ru="in отвечает да или нет; find даёт позицию и -1 вместо исключения, в отличие от index."),
            dict(title_en="f-strings and format specs", title_ru="f-строки и спецификаторы формата",
                 code='name, price, share = "rye", 2.5, 0.375\nf"{name:<10}|{price:>8.2f}|"        # \'rye       |    2.50|\'\nf"{share:.1%}"                      # \'37.5%\'\nf"{1234567:,}"                      # \'1,234,567\'\nf"{name!r} costs {price=}"          # "\'rye\' costs price=2.5"\n',
                 note_en="Inside the braces: [fill][align][width][,][.precision][type]. < left, > right, ^ centre.",
                 note_ru="Внутри фигурных скобок: [заполнитель][выравнивание][ширина][,][.точность][тип]. < влево, > вправо, ^ по центру."),
            dict(title_en="Slicing and characters", title_ru="Срезы и символы",
                 code='word = "phoenix"\nword[0], word[-1], word[1:4], word[::-1]   # \'p\', \'x\', \'hoe\', \'xineohp\'\nord("a"), chr(98)                          # 97, \'b\'\n"".join(sorted("cab"))                     # \'abc\'\n"7".isdigit(), "Ab".isalpha()              # True, True\n',
                 note_en="Strings slice like lists. ord and chr give the code point, which is how Caesar shifts and letter maths work.",
                 note_ru="Строки режутся как списки. ord и chr дают код символа – на этом строятся шифр Цезаря и арифметика букв."),
        ],
        gotchas_en=[
            "Strings are immutable: sign.upper() returns a new string and leaves sign unchanged.",
            "'a' + 1 raises TypeError: convert with str(1) or use an f-string.",
            "split(',') keeps empty pieces and surrounding spaces; strip each piece, or use split() for whitespace.",
        ],
        gotchas_ru=[
            "Строки неизменяемы: sign.upper() возвращает новую строку, а sign остаётся прежней.",
            "'a' + 1 бросает TypeError: преобразуй через str(1) или используй f-строку.",
            "split(',') оставляет пустые куски и пробелы вокруг; делай strip каждому куску или используй split() по пробелам.",
        ],
        phrase_en="I'll normalise the input first: strip and lowercase, then compare.",
    ),
)
