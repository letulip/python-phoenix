META = dict(
    id="l0.collections.unique-viewers", type="cloze", order=30,
    difficulty=1, minutes=2, world="shorts",
    concepts=["set-basics", "in-operator", "len"],
    story_en="The Shorts dashboard counts six views. Pixel counts three humans. Pixel is right.",
    title="Unique viewers",
    statement_en="Fill in the blanks so that unique holds each viewer once, how_many is 3 and bob_was_here is True.",
    hints_en=["The built-in that drops duplicates is set(...). Membership is the in operator."],
    hints_ru=["Встроенная функция, убирающая дубликаты, – set(...). Проверка вхождения – оператор in."],
    explanation_en="set(list) keeps one copy of every value; len counts members and 'in' is a constant-time check.",
    explanation_ru="set(list) оставляет по одной копии каждого значения; len считает элементы, а in проверяет вхождение за константное время.",
)

STARTER = '''
viewers = ["ann", "bob", "ann", "cid", "bob", "ann"]
unique = ___(viewers)
how_many = len(unique)        # 3
bob_was_here = "bob" ___ unique
'''

SOLUTION = '''
viewers = ["ann", "bob", "ann", "cid", "bob", "ann"]
unique = set(viewers)
how_many = len(unique)
bob_was_here = "bob" in unique
'''

TESTS = '''
def test_unique_is_a_set(ns, check):
    check(type(ns["unique"]), set, "type(unique)")

def test_unique_members(ns, check):
    check(ns["unique"], {"ann", "bob", "cid"}, "unique")

def test_count_and_membership(ns, check):
    check((ns["how_many"], ns["bob_was_here"]), (3, True), "how_many, bob_was_here")
'''
