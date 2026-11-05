META = dict(
    id="l0.loops.find-the-stowaway", type="retype", order=40,
    difficulty=2, minutes=4, world="game",
    concepts=["for-loop", "break-continue", "for-else", "early-return"],
    story_en="Someone on the belt is not on the crew list. Byte suspects the parrot. The parrot retired.",
    title="Find the stowaway",
    statement_en=("Retype both functions: the first returns early from inside a loop, the second uses break and the loop's "
                  "else clause, which runs only when the loop finished without a break."),
    hints_en=["return inside a loop ends the whole function. for ... else: the else body runs only if no break happened."],
    hints_ru=["return внутри цикла завершает всю функцию. for ... else: тело else выполняется, только если break не случился."],
    explanation_en=("Early return is the clean way to 'search and stop'. The for-else form says 'if we got through everyone "
                    "without breaking, there was no stowaway'; after a break, name still holds the culprit."),
    explanation_ru=("Ранний return – чистый способ «найти и остановиться». Форма for-else говорит: «если прошли всех без break, "
                    "безбилетника нет»; после break переменная name всё ещё хранит виновника."),
)

MODEL = '''
def first_negative(numbers):
    for n in numbers:
        if n < 0:
            return n
    return None

def find_stowaway(crew, allowed):
    for name in crew:
        if name not in allowed:
            break
    else:
        return None
    return name
'''

STARTER = ""

TESTS = '''
def test_first_negative(ns, check):
    check(ns["first_negative"]([3, -2, -5]), -2, "first_negative([3, -2, -5])")

def test_no_negative(ns, check):
    check(ns["first_negative"]([1, 2]), None, "first_negative([1, 2])")

def test_stowaway_found(ns, check):
    check(ns["find_stowaway"](["Pixel", "Byte", "Ghost"], {"Pixel", "Byte"}), "Ghost", "find_stowaway with a ghost aboard")

def test_no_stowaway(ns, check):
    check(ns["find_stowaway"](["Pixel"], {"Pixel"}), None, "find_stowaway with everyone allowed")
'''
