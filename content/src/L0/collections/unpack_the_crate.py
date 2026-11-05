META = dict(
    id="l0.collections.unpack-the-crate", type="retype", order=40,
    difficulty=1, minutes=3, world="game",
    concepts=["tuple-unpacking", "none-check", "truthiness"],
    story_en="Captain Byte's crates come with a note. Sometimes the note is None, which is pirate for 'figure it out'.",
    title="Unpack the crate",
    statement_en="Retype the snippet: unpack a tuple into three names, replace a None note, and use truthiness of an empty list.",
    hints_en=["Three names on the left, one tuple on the right. Compare with None using 'is'. An empty list is falsy, so 'if not items' works."],
    hints_ru=["Три имени слева, один кортеж справа. С None сравнивай через is. Пустой список ложен, поэтому работает if not items."],
    explanation_en="Unpacking reads better than crate[0], crate[1], crate[2]. 'is None' is the idiom because None is a single object. Empty containers are falsy, so you never write len(items) == 0.",
    explanation_ru="Распаковка читается лучше, чем crate[0], crate[1], crate[2]. is None – идиома, потому что None единственный объект. Пустые контейнеры ложны, поэтому len(items) == 0 не пишут.",
)

MODEL = '''
crate = ("gold", 12, None)
kind, amount, note = crate
if note is None:
    note = "no note"

items = []
if not items:
    status = "empty"
else:
    status = f"{len(items)} items"
'''

STARTER = ""

TESTS = '''
def test_unpacked(ns, check):
    check((ns["kind"], ns["amount"]), ("gold", 12), "kind, amount")

def test_note_replaced(ns, check):
    check(ns["note"], "no note", "note")

def test_status(ns, check):
    check(ns["status"], "empty", "status")
'''
