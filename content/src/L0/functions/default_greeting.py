META = dict(
    id="l0.functions.default-greeting", type="cloze", order=20,
    difficulty=1, minutes=2, world="game",
    concepts=["default-args", "def-return"],
    story_en="Nobody on Byte's ship says 'Hello'. It is 'Ahoy' or nothing, unless the captain insists otherwise.",
    title="Ahoy by default",
    statement_en=("Pirates say 'Ahoy' unless told otherwise. Fill in the blank so that welcome('Pixel') returns "
                  "'Ahoy, Pixel!' and welcome('Pixel', 'Hi') returns 'Hi, Pixel!'."),
    hints_en=["The blank is a default value for greeting, so it must be a string literal."],
    hints_ru=["Пропуск – это значение по умолчанию для greeting, значит там строковый литерал."],
    explanation_en="A default argument fills in when the caller passes nothing; an explicit argument overrides it.",
    explanation_ru="Аргумент по умолчанию подставляется, когда вызывающий ничего не передал; явный аргумент его перекрывает.",
)

STARTER = '''
def welcome(name, greeting=___):
    return f"{greeting}, {name}!"

# welcome("Pixel")        -> "Ahoy, Pixel!"
# welcome("Pixel", "Hi")  -> "Hi, Pixel!"
'''

SOLUTION = '''
def welcome(name, greeting="Ahoy"):
    return f"{greeting}, {name}!"
'''

TESTS = '''
def test_default(ns, check):
    check(ns["welcome"]("Pixel"), "Ahoy, Pixel!", "welcome('Pixel')")

def test_override(ns, check):
    check(ns["welcome"]("Pixel", "Hi"), "Hi, Pixel!", "welcome('Pixel', 'Hi')")

def test_keyword(ns, check):
    check(ns["welcome"]("Byte", greeting="Yo"), "Yo, Byte!", "welcome('Byte', greeting='Yo')")
'''
