META = dict(
    id="l0.loops.numbered-lines", type="cloze", order=20,
    difficulty=1, minutes=2, world="game",
    concepts=["enumerate", "for-loop"],
    story_en="Byte's crew list must be numbered from 1. Pirates do not start counting at zero; only Pixel does.",
    title="Numbered lines",
    statement_en="Fill in the blanks so the loop yields a running number together with each name, counting from 1. Use the built-in made for exactly this.",
    hints_en=["enumerate(items, start=1) yields (number, item) pairs."],
    hints_ru=["enumerate(items, start=1) выдаёт пары (номер, элемент)."],
    explanation_en="enumerate removes the manual counter: no i = 0 before the loop and no i += 1 inside. The start argument sets the first number.",
    explanation_ru="enumerate убирает ручной счётчик: ни i = 0 до цикла, ни i += 1 внутри. Аргумент start задаёт первый номер.",
)

STARTER = '''
crew = ["Pixel", "Byte", "Ada"]
lines = []
for number, name in ___(crew, start=___):
    lines.append(f"{number}. {name}")
# lines == ["1. Pixel", "2. Byte", "3. Ada"]
'''

SOLUTION = '''
crew = ["Pixel", "Byte", "Ada"]
lines = []
for number, name in enumerate(crew, start=1):
    lines.append(f"{number}. {name}")
'''

TESTS = '''
def test_lines(ns, check):
    check(ns["lines"], ["1. Pixel", "2. Byte", "3. Ada"], "lines")

def test_uses_enumerate(src, ast_tools, check):
    check(ast_tools.uses_name(src, "enumerate"), True, "enumerate is used")
'''
