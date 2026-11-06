META = dict(
    id="l0.functions.extract-helper", type="refactor", order=80,
    difficulty=2, minutes=6, world="everyday",
    concepts=["extract-function", "def-return", "call-function"],
    story_en="Grandma Ada's receipt printer prints three lines. She would like to buy a fourth item someday.",
    title="Extract the repeated receipt line",
    statement_en=("print_receipt(items) prints a receipt; items is a list of (name, qty, price) tuples. "
                  "Three lines of the function are copy-pasted. Extract the repeated formatting into a helper "
                  "format_line(name, qty, price) that returns the string, and make print_receipt a loop with a single "
                  "print call. The printed output must not change."),
    hints_en=[
        "Find the three lines that differ only in the data they use: the index 0, 1, 2.",
        "Define format_line(name, qty, price) above print_receipt and make it return the f-string, not print it.",
        "Replace the three prints with: for name, qty, price in items: print(format_line(name, qty, price)).",
    ],
    hints_ru=[
        "Найди три строки, которые отличаются только данными: индексами 0, 1, 2.",
        "Объяви format_line(name, qty, price) над print_receipt и верни из неё f-строку, а не печатай.",
        "Замени три print одним циклом: for name, qty, price in items: print(format_line(name, qty, price)).",
    ],
    explanation_en=("Repetition is the cue for a function: the shared part becomes the body, the differences become "
                    "parameters. The helper returns the string instead of printing, so it is testable and reusable. "
                    "The loop with tuple unpacking also removes the hidden assumption of exactly three items."),
    explanation_ru=("Повтор – сигнал к функции: общее уходит в тело, различия становятся параметрами. "
                    "Вспомогательная функция возвращает строку, а не печатает, поэтому её можно проверить тестом и "
                    "переиспользовать. Цикл с распаковкой кортежа заодно убирает скрытое допущение о ровно трёх позициях."),
    talk_track=[
        "Name what repeats and what varies between the three lines.",
        "Say the helper returns a string, so it is easy to unit-test.",
        "Mention the loop removes the hard-coded assumption of exactly three items.",
    ],
    complexity="O(n) in the number of items",
    followups=["Where would you add a total line?", "What if an item has a quantity of zero?"],
)

STARTER = '''
def print_receipt(items):
    print(f"{items[0][0]:<10} x{items[0][1]:>2}  {items[0][1] * items[0][2]:>7.2f}")
    print(f"{items[1][0]:<10} x{items[1][1]:>2}  {items[1][1] * items[1][2]:>7.2f}")
    print(f"{items[2][0]:<10} x{items[2][1]:>2}  {items[2][1] * items[2][2]:>7.2f}")
'''

EXAMPLES = [
    {"call": "print_receipt([('tea', 2, 1.5), ('milk', 1, 2.25), ('bread', 3, 0.8)])",
     "prints": "tea        x 2     3.00\nmilk       x 1     2.25\nbread      x 3     2.40"},
]

SOLUTION = '''
def format_line(name, qty, price):
    return f"{name:<10} x{qty:>2}  {qty * price:>7.2f}"

def print_receipt(items):
    for name, qty, price in items:
        print(format_line(name, qty, price))
'''

TESTS = '''
ITEMS = [("tea", 2, 1.5), ("milk", 1, 2.25), ("bread", 3, 0.8)]

def test_helper_defined(ns, check):
    check(callable(ns.get("format_line")), True, "format_line is defined")

def test_helper_returns_line(ns, check):
    check(ns["format_line"]("tea", 2, 1.5), "tea        x 2     3.00", "format_line('tea', 2, 1.5)")

def test_output_unchanged(ns, check, capture):
    out = capture(ns["print_receipt"], ITEMS)
    check(out.splitlines(),
          ["tea        x 2     3.00", "milk       x 1     2.25", "bread      x 3     2.40"],
          "printed lines")

def test_works_for_four_items(ns, check, capture):
    out = capture(ns["print_receipt"], ITEMS + [("jam", 1, 4.0)])
    check(len(out.splitlines()), 4, "four items print four lines")

def test_duplication_removed(src, ast_tools, check):
    check(ast_tools.count_calls(src, "format_line") >= 1, True, "print_receipt calls format_line")
    check(ast_tools.count_fstrings(src) <= 1, True, "only one f-string is left")
    check(ast_tools.count_calls(src, "print") <= 1, True, "a single print call inside a loop")
    check(ast_tools.has_loop(src), True, "print_receipt uses a loop")
'''

LEVELS = dict(
    middle=dict(
        note_en=("The repeated line became format_line and print_receipt loops with tuple unpacking: the duplication is "
                 "gone and a fourth item costs nothing. What an interviewer still notices: print_receipt both computes "
                 "the text and prints it, so the only way to test it is to capture stdout, and reusing the lines "
                 "elsewhere (a file, a window) means touching the function again."),
        note_ru=("Повторяющаяся строка стала format_line, а print_receipt идёт циклом с распаковкой: дублирование ушло, "
                 "четвёртая позиция ничего не стоит. Что интервьюер всё ещё видит: print_receipt одновременно считает "
                 "текст и печатает его, поэтому проверить его можно только перехватом stdout, а переиспользовать строки "
                 "(файл, окно) – значит снова лезть в функцию."),
    ),
    senior=dict(
        code='''
def format_line(name, qty, price):
    return f"{name:<10} x{qty:>2}  {qty * price:>7.2f}"

def receipt_lines(items):
    return [format_line(name, qty, price) for name, qty, price in items]

def print_receipt(items):
    for line in receipt_lines(items):
        print(line)
''',
        note_en=("Keeps the I/O at the edge: receipt_lines is a pure function that returns the text and print_receipt is a "
                 "two-line shell around it. Pure functions are trivial to unit-test and to reuse, which is what "
                 "'testable design' means when an interviewer says it. And not one step further: no class, no template "
                 "engine, no configuration object. Knowing where to stop is part of the level."),
        note_ru=("Ввод-вывод вынесен на край: receipt_lines – чистая функция, которая возвращает текст, а print_receipt – "
                 "двухстрочная оболочка вокруг неё. Чистые функции тривиально тестировать и переиспользовать; именно это "
                 "интервьюер имеет в виду под «testable design». И ни шагом дальше: без класса, без шаблонизатора, без "
                 "объекта настроек. Умение остановиться – тоже часть уровня."),
    ),
)
