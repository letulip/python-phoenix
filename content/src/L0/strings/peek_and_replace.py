META = dict(
    id="l0.strings.peek-and-replace", type="retype", order=40,
    difficulty=1, minutes=3, world="everyday",
    concepts=["find-in", "replace", "str-case", "string-slicing"],
    story_en="The storm left the signboard SHOUTING. Ada wants it to speak normally and to say that bread is baked every day.",
    title="Peek and replace",
    statement_en="Retype the snippet: membership with in, position with find, a case change, a replace, and two slices of the sign.",
    hints_en=["find returns the index of the first match. replace returns a new string; the original stays as it was."],
    hints_ru=["find возвращает индекс первого совпадения. replace возвращает новую строку; исходная остаётся прежней."],
    explanation_en="None of these calls change sign: strings are immutable, so each method hands back a new value and you store it under a new name.",
    explanation_ru="Ни один из вызовов не меняет sign: строки неизменяемы, поэтому каждый метод отдаёт новое значение, которое ты сохраняешь под новым именем.",
)

MODEL = '''
sign = "Ada's Bakery: fresh bread daily"
has_bread = "bread" in sign
where = sign.find("fresh")
shouting = sign.upper()
fixed = sign.replace("daily", "every day")
first_word = sign[:5]
last_word = sign[-5:]
'''

STARTER = ""

TESTS = '''
def test_membership_and_position(ns, check):
    check((ns["has_bread"], ns["where"]), (True, 14), "has_bread, where")

def test_shouting(ns, check):
    check(ns["shouting"], "ADA'S BAKERY: FRESH BREAD DAILY", "shouting")

def test_fixed(ns, check):
    check(ns["fixed"], "Ada's Bakery: fresh bread every day", "fixed")

def test_slices(ns, check):
    check((ns["first_word"], ns["last_word"]), ("Ada's", "daily"), "first_word, last_word")

def test_sign_untouched(ns, check):
    check(ns["sign"], "Ada's Bakery: fresh bread daily", "sign unchanged")
'''
