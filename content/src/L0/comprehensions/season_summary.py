META = dict(
    id="l0.comprehensions.season-summary", type="task", order=68,
    difficulty=2, minutes=6, world="tennis",
    concepts=["min-max-key", "sum", "any-all", "lambda"],
    story_en="Coach Topspin wants the season on one index card: the marathon match, the total games for the knees, and whether anyone can say 'undefeated' with a straight face.",
    title="Season summary",
    statement_en=("Write season_summary(matches) -> dict. matches is a list of dicts with keys 'opponent', 'games' and "
                  "'won' (bool). Return {'longest': the opponent of the match with the most games (the first one on a "
                  "tie), 'total': the sum of games, 'all_won': True when every match was won}. For an empty season "
                  "return {'longest': None, 'total': 0, 'all_won': True}: with no match lost, 'all won' holds."),
    hints_en=[
        "max(matches, key=lambda m: m['games']) returns the whole match dict; take its 'opponent'.",
        "sum(m['games'] for m in matches) and all(m['won'] for m in matches) do the other two in one line each.",
        "Handle the empty list before calling max, or use max(..., default=None).",
    ],
    hints_ru=[
        "max(matches, key=lambda m: m['games']) возвращает весь словарь матча; возьми его 'opponent'.",
        "sum(m['games'] for m in matches) и all(m['won'] for m in matches) делают остальные два по одной строке.",
        "Пустой список обработай до вызова max или используй max(..., default=None).",
    ],
    explanation_en=("Three questions, three built-ins: max with a key finds the longest match and keeps the first on a "
                    "tie, sum adds a generator without a temporary list, all answers 'every one?' and is True for an "
                    "empty season because no match contradicts it. Only max needs the empty case handled."),
    explanation_ru=("Три вопроса, три встроенные функции: max с ключом находит самый длинный матч и при ничьей "
                    "оставляет первый, sum складывает генератор без временного списка, all отвечает «все ли?» и для "
                    "пустого сезона даёт True, потому что ни один матч этому не противоречит. Пустой случай нужен только max."),
    talk_track=[
        "Say max with a key returns the element, not the key value, so you can read its opponent.",
        "Point out all([]) is True by definition and that the statement asks for exactly that.",
        "Mention three passes over the list are O(n) and fine; one merged loop is not worth the readability.",
    ],
    complexity="O(n)",
    followups=["Add the win rate as a percentage.", "What if 'games' is missing for an unfinished match?"],
)

STARTER = '''
def season_summary(matches):
    ...
'''

EXAMPLES = [
    {"call": "season_summary([{'opponent': 'Ada', 'games': 12, 'won': True}, {'opponent': 'Byte', 'games': 18, 'won': False}])",
     "expected": "{'longest': 'Byte', 'total': 30, 'all_won': False}"},
    {"call": "season_summary([])", "expected": "{'longest': None, 'total': 0, 'all_won': True}"},
]

SOLUTION = '''
def season_summary(matches):
    if not matches:
        return {"longest": None, "total": 0, "all_won": True}
    longest = max(matches, key=lambda m: m["games"])
    return {
        "longest": longest["opponent"],
        "total": sum(m["games"] for m in matches),
        "all_won": all(m["won"] for m in matches),
    }
'''

TESTS = '''
SEASON = [
    {"opponent": "Ada", "games": 12, "won": True},
    {"opponent": "Byte", "games": 18, "won": False},
    {"opponent": "Cid", "games": 9, "won": True},
]

def test_season(ns, check):
    check(ns["season_summary"](SEASON), {"longest": "Byte", "total": 39, "all_won": False}, "season_summary(SEASON)")

def test_empty_season(ns, check):
    check(ns["season_summary"]([]), {"longest": None, "total": 0, "all_won": True}, "season_summary([])")

def test_all_won(ns, check):
    wins = [{"opponent": "Ada", "games": 10, "won": True}, {"opponent": "Cid", "games": 8, "won": True}]
    check(ns["season_summary"](wins)["all_won"], True, "all_won when every match was won")

def test_tie_keeps_first(ns, check):
    tie = [{"opponent": "First", "games": 15, "won": True}, {"opponent": "Second", "games": 15, "won": True}]
    check(ns["season_summary"](tie)["longest"], "First", "the first of two equally long matches")

def test_keys(ns, check):
    check(sorted(ns["season_summary"](SEASON)), ["all_won", "longest", "total"], "exactly the three keys")
'''

LEVELS = dict(
    middle=dict(
        code='''
def season_summary(matches):
    longest = None
    most_games = -1
    total = 0
    all_won = True
    for m in matches:
        if m["games"] > most_games:
            most_games = m["games"]
            longest = m["opponent"]
        total = total + m["games"]
        if not m["won"]:
            all_won = False
    return {"longest": longest, "total": total, "all_won": all_won}
''',
        note_en=("One pass, four variables, every rule handled by hand: correct, including the empty season, because the "
                 "starting values were chosen with care. It reads like C. The three questions, max by key, sum and all, "
                 "each have a built-in that says the question in one word, and the interviewer is waiting to hear them."),
        note_ru=("Один проход, четыре переменные, каждое правило вручную: верно, включая пустой сезон, потому что "
                 "начальные значения выбраны аккуратно. Читается как C. У трёх вопросов – max по ключу, sum и all – есть "
                 "встроенные функции, которые называют вопрос одним словом, и интервьюер ждёт, когда их услышит."),
    ),
    senior=dict(
        code='''
def season_summary(matches):
    """Opponent of the longest match (first on a tie), total games, and whether every match was won."""
    longest = max(matches, key=lambda m: m["games"], default=None)
    return {
        "longest": longest["opponent"] if longest else None,
        "total": sum(m["games"] for m in matches),
        "all_won": all(m["won"] for m in matches),
    }
''',
        note_en=("Three built-ins, three lines, and max(..., default=None) removes the special case for an empty season. "
                 "The vacuous truth of all([]) is stated as intended in the docstring instead of being an accident. A "
                 "senior says three O(n) passes are fine and would merge them only if profiling asked, and mentions a "
                 "dataclass for a match would replace the string keys."),
        note_ru=("Три встроенные функции, три строки, а max(..., default=None) убирает особый случай пустого сезона. "
                 "Пустая истинность all([]) заявлена в докстринге как задуманная, а не как случайность. Сеньор говорит, "
                 "что три прохода O(n) – нормально, и объединил бы их в один цикл только по данным профилировщика, а "
                 "ещё упоминает, что dataclass для матча заменил бы строковые ключи."),
    ),
)
