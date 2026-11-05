MODULE = dict(
    id="l0.functions", level=0, order=1,
    title_en="Functions", title_ru="Функции",
    concepts=["def-return", "default-args", "star-args", "kwargs", "early-return",
              "docstring", "extract-function", "call-function"],
    diagnostic=["l0.functions.cat-years"],
    chapter_en="Act I · Chapter 1: The toolbox", chapter_ru="Акт I · Глава 1: Ящик с инструментами",
    story_en=("Purrfect Code, the tiny software studio of Pixel the cat, has stood dark for three years. "
              "You are the engineer who came back to switch the lights on. Pixel hands you a dusty toolbox: "
              "every tool inside is a function, and half of them have forgotten what they return."),
    story_ru=("Purrfect Code, крошечная студия кота Пикселя, три года стояла без света. "
              "Ты – инженер, который вернулся включить рубильник. Пиксель протягивает пыльный ящик с инструментами: "
              "каждый инструмент – функция, и половина из них забыла, что должна возвращать."),
    story_done_en="The toolbox clicks shut. Pixel purrs: the studio has power again, and Captain Byte is already knocking.",
    story_done_ru="Ящик защёлкивается. Пиксель урчит: в студии снова есть свет, а капитан Байт уже стучит в дверь.",
    card=dict(
        intro_en=("A function is a named recipe: inputs arrive as parameters, one result leaves through "
                  "return. Anything that repeats, or simply deserves a name, becomes a function."),
        intro_ru=("Функция – рецепт с именем: входы приходят параметрами, результат уходит через return. "
                  "Всё, что повторяется или просто заслуживает имени, становится функцией."),
        snippets=[
            dict(title_en="Define and return", title_ru="Объявить и вернуть",
                 code='def area(width, height):\n    """Return the area of a rectangle."""\n    return width * height\n\nprint(area(3, 4))   # 12\n',
                 note_en="print shows a value on screen; return hands it back to the caller. A function without return gives None.",
                 note_ru="print показывает значение на экране, return отдаёт его вызывающему. Функция без return возвращает None."),
            dict(title_en="Default arguments", title_ru="Аргументы по умолчанию",
                 code='def greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\ngreet("Pixel")                   # \'Hello, Pixel!\'\ngreet("Pixel", "Ahoy")           # \'Ahoy, Pixel!\'\ngreet(greeting="Yo", name="Byte")  # keywords in any order\n',
                 note_en="Parameters with defaults go after the ones without. Keyword arguments can come in any order.",
                 note_ru="Параметры с умолчаниями идут после обычных. Именованные аргументы можно передавать в любом порядке."),
            dict(title_en="*args and **kwargs", title_ru="*args и **kwargs",
                 code='def total(*numbers):        # numbers is a tuple\n    return sum(numbers)\n\ndef show(**fields):         # fields is a dict\n    for key, value in fields.items():\n        print(key, "=", value)\n\ntotal(1, 2, 3)              # 6\nshow(name="Pixel", age=3)   # name = Pixel / age = 3\n',
                 note_en="One star packs positional extras into a tuple, two stars pack keyword extras into a dict.",
                 note_ru="Одна звёздочка собирает лишние позиционные аргументы в кортеж, две – именованные в словарь."),
            dict(title_en="Early return", title_ru="Ранний return",
                 code='def can_vote(age, citizen):\n    if not citizen:\n        return False     # leave early, no else needed\n    return age >= 18\n',
                 note_en="Handle the special case first and return; the main path stays flat and readable.",
                 note_ru="Сначала обработай особый случай и выйди; основной путь остаётся плоским и читаемым."),
            dict(title_en="Extract a helper", title_ru="Вынести вспомогательную функцию",
                 code='def line(name, qty):\n    return f"{name:<8}{qty:>3}"\n\ndef receipt(items):\n    for name, qty in items:\n        print(line(name, qty))\n',
                 note_en="What repeats goes into the body, what differs becomes parameters. Return the string, print it elsewhere.",
                 note_ru="Что повторяется – в тело функции, что различается – в параметры. Строку возвращаем, печатаем снаружи."),
        ],
        gotchas_en=[
            "A mutable default (def add(item, items=[])) is shared between calls. Use None and create the list inside.",
            "Forgetting return makes the function give None, so print(double(2)) prints None.",
            "A default parameter cannot come before a parameter without a default.",
        ],
        gotchas_ru=[
            "Изменяемое умолчание (def add(item, items=[])) общее для всех вызовов. Ставь None и создавай список внутри.",
            "Забытый return означает, что функция вернёт None, и print(double(2)) напечатает None.",
            "Параметр с умолчанием нельзя ставить перед параметром без умолчания.",
        ],
        phrase_en="I'll pull this into a helper so the main function reads top-down.",
    ),
)
