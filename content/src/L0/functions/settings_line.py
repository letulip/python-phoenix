META = dict(
    id="l0.functions.settings-line", type="task", order=68,
    difficulty=2, minutes=5, world="shorts",
    concepts=["kwargs", "early-return", "def-return"],
    story_en="Pixel's streaming setup has eleven knobs. The overlay should list the ones that were touched in a tidy row, or say 'defaults'.",
    title="Settings line",
    statement_en=("Write settings_line(**options) -> str. It accepts any keyword arguments and returns them as 'key=value' "
                  "pairs joined with ', ', sorted by key. With no arguments it returns 'defaults'. "
                  "Example: settings_line(res='1080p', fps=60) -> 'fps=60, res=1080p'."),
    hints_en=[
        "**options arrives as a dict; the empty-dict case is the early return with 'defaults'.",
        "sorted(options.items()) gives (key, value) pairs in key order.",
        "Build the pieces as f'{key}={value}' and join them with ', '.",
    ],
    hints_ru=[
        "**options приходит словарём; пустой словарь – ранний return с 'defaults'.",
        "sorted(options.items()) даёт пары (ключ, значение) в порядке ключей.",
        "Собери кусочки как f'{key}={value}' и соедини через ', '.",
    ],
    explanation_en=("Inside the function **options is an ordinary dict, so sorting and joining are the ordinary dict tools. "
                    "Sorting by key makes the output deterministic whatever order the caller used; the empty case gets "
                    "its own early return so the join never has to deal with it."),
    explanation_ru=("Внутри функции **options – обычный словарь, так что сортировка и склейка – обычные инструменты словаря. "
                    "Сортировка по ключу делает вывод детерминированным при любом порядке вызова; пустой случай получает "
                    "свой ранний return, чтобы join с ним не возился."),
    talk_track=[
        "Say **options is a dict and that you sort it so the output does not depend on call order.",
        "Mention the empty case returns a word instead of an empty string.",
        "Note that ', '.join avoids a trailing separator.",
    ],
    complexity="O(k log k) for k options",
    followups=["How would you hide options that still hold their default value?", "What if a value contains a comma?"],
)

STARTER = '''
def settings_line(**options):
    ...
'''

EXAMPLES = [
    {"call": "settings_line(res='1080p', fps=60)", "expected": "'fps=60, res=1080p'"},
    {"call": "settings_line()", "expected": "'defaults'"},
]

SOLUTION = '''
def settings_line(**options):
    if not options:
        return "defaults"
    parts = []
    for key, value in sorted(options.items()):
        parts.append(f"{key}={value}")
    return ", ".join(parts)
'''

TESTS = '''
def test_two_options_sorted(ns, check):
    check(ns["settings_line"](res="1080p", fps=60), "fps=60, res=1080p", "settings_line(res='1080p', fps=60)")

def test_empty(ns, check):
    check(ns["settings_line"](), "defaults", "settings_line()")

def test_single(ns, check):
    check(ns["settings_line"](mic="on"), "mic=on", "settings_line(mic='on')")

def test_three_keys(ns, check):
    check(ns["settings_line"](c=3, a=1, b=2), "a=1, b=2, c=3", "keys sorted")

def test_accepts_keywords_only(ns, check):
    import inspect
    kinds = [p.kind for p in inspect.signature(ns["settings_line"]).parameters.values()]
    check(kinds, [inspect.Parameter.VAR_KEYWORD], "the only parameter is **options")
'''

LEVELS = dict(
    middle=dict(
        code='''
def settings_line(**options):
    if len(options) == 0:
        return "defaults"
    result = ""
    for key in sorted(options.keys()):
        result += key + "=" + str(options[key]) + ", "
    return result[:-2]
''',
        note_en=("It passes, but look at the seams: the separator is appended every time and then cut off with [:-2], the "
                 "classic home of an off-by-one. len(options) == 0 works where 'if not options' is the idiom, and str() "
                 "plus + is the hard way to format. Each is small; together they are what 'middle' looks like to a reviewer."),
        note_ru=("Проходит, но видны швы: разделитель добавляется каждый раз и потом отрезается через [:-2] – классический дом "
                 "ошибки на единицу. len(options) == 0 работает там, где идиома – if not options, а str() и + – тяжёлый способ "
                 "форматировать. Каждая мелочь мала; вместе они и есть «middle» в глазах ревьюера."),
    ),
    senior=dict(
        code='''
def settings_line(**options):
    """'key=value' pairs sorted by key, or 'defaults' when nothing was set."""
    if not options:
        return "defaults"
    return ", ".join(f"{key}={value}" for key, value in sorted(options.items()))
''',
        note_en=("One early return for the empty case, then one expression that says exactly what the output is: sorted "
                 "pairs, formatted, joined. join puts separators between items, so there is nothing to trim. A senior also "
                 "says why the sort is there (a deterministic line) and asks whether values with commas need quoting "
                 "before promising this format to anyone."),
        note_ru=("Один ранний return для пустого случая, потом одно выражение, которое буквально описывает результат: "
                 "отсортированные пары, отформатированы, склеены. join ставит разделители между элементами, обрезать нечего. "
                 "Сеньор ещё объясняет, зачем сортировка (детерминированная строка), и спрашивает, надо ли экранировать "
                 "значения с запятыми, прежде чем обещать кому-то этот формат."),
    ),
)
