META = dict(
    id="l0.functions.loot-splitter", type="retype", order=40,
    difficulty=2, minutes=4, world="game",
    concepts=["star-args", "kwargs", "docstring", "def-return"],
    story_en="Three chests today, eleven tomorrow. Byte wants one function that does not care how many.",
    title="Loot splitter",
    statement_en=("Captain Byte never knows how many chests the crew will drag aboard. Retype the two functions "
                  "exactly: one takes any number of chests with *chests, the other any number of name=share pairs "
                  "with **crew."),
    hints_en=["*chests collects positional arguments into a tuple; **crew collects keyword arguments into a dict, iterate it with .items()."],
    hints_ru=["*chests собирает позиционные аргументы в кортеж; **crew собирает именованные в словарь, обходи его через .items()."],
    explanation_en=("The star syntax lets a function accept a flexible number of inputs. "
                    "Inside, chests is just a tuple and crew is just a dict: ordinary loops apply."),
    explanation_ru=("Звёздочки позволяют функции принимать переменное число входов. "
                    "Внутри chests – обычный кортеж, а crew – обычный словарь, с ними работают обычные циклы."),
)

MODEL = '''
def total_loot(*chests):
    """Sum any number of chests; each chest is a number of coins."""
    total = 0
    for coins in chests:
        total += coins
    return total

def shares(**crew):
    """crew holds name=share pairs; return 'name: share' lines."""
    lines = []
    for name, share in crew.items():
        lines.append(f"{name}: {share}")
    return lines
'''

STARTER = ""

TESTS = '''
def test_total_three_chests(ns, check):
    check(ns["total_loot"](10, 20, 5), 35, "total_loot(10, 20, 5)")

def test_total_no_chests(ns, check):
    check(ns["total_loot"](), 0, "total_loot()")

def test_shares_two(ns, check):
    check(ns["shares"](Pixel=10, Byte=25), ["Pixel: 10", "Byte: 25"], "shares(Pixel=10, Byte=25)")

def test_shares_none(ns, check):
    check(ns["shares"](), [], "shares()")
'''
