META = dict(
    id="l0.functions.early-exit", type="cloze", order=30,
    difficulty=1, minutes=3, world="game",
    concepts=["early-return", "def-return"],
    story_en="The pirate cruise has a bouncer: a very large crab with a clipboard and two rules.",
    title="Who boards the pirate cruise",
    statement_en=("The pirate cruise has two rules: nobody under 12 boards, everyone else needs a ticket. "
                  "Fill in both blanks so can_board returns True or False accordingly."),
    hints_en=["The first blank is a value for the special case. The second blank is the ticket itself: has_ticket is already a bool."],
    hints_ru=["Первый пропуск – значение для особого случая. Второй пропуск – сам билет: has_ticket уже является bool."],
    explanation_en=("Early return handles the exception first, then the normal rule stands alone. "
                    "Returning has_ticket directly beats 'if has_ticket: return True else: return False'."),
    explanation_ru=("Ранний return сначала обрабатывает исключение из правила, а потом остаётся само правило. "
                    "Вернуть has_ticket напрямую лучше, чем писать if has_ticket: return True else: return False."),
)

STARTER = '''
def can_board(age, has_ticket):
    """Under 12: never. Otherwise: only with a ticket."""
    if age < 12:
        return ___
    return ___
'''

SOLUTION = '''
def can_board(age, has_ticket):
    """Under 12: never. Otherwise: only with a ticket."""
    if age < 12:
        return False
    return has_ticket
'''

TESTS = '''
def test_too_young(ns, check):
    check(ns["can_board"](8, True), False, "can_board(8, True)")

def test_adult_with_ticket(ns, check):
    check(ns["can_board"](30, True), True, "can_board(30, True)")

def test_adult_without_ticket(ns, check):
    check(ns["can_board"](30, False), False, "can_board(30, False)")

def test_exactly_twelve(ns, check):
    check(ns["can_board"](12, True), True, "can_board(12, True)")

def test_returns_bool(ns, check):
    check(type(ns["can_board"](40, False)), bool, "type(can_board(40, False))")
'''
