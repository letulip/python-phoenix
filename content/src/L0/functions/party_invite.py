META = dict(
    id="l0.functions.party-invite", type="task", order=70,
    difficulty=2, minutes=7, world="game",
    concepts=["star-args", "default-args", "def-return"],
    story_en="Pixel is throwing a studio reopening party and refuses to write invitations by paw.",
    title="Party invite",
    statement_en=("Write invite(name, *friends, host='Pixel') -> str. It returns '<host> invites <guests> to the party!' "
                  "where guests lists name and all friends: one guest 'Bob', two guests 'Bob and Ann', "
                  "three or more 'Bob, Ann and Tom' (commas, then 'and' before the last). "
                  "Example: invite('Bob', 'Ann', host='Byte') -> 'Byte invites Bob and Ann to the party!'"),
    hints_en=[
        "Build the full guest list first: guests = [name, *friends] or [name] + list(friends).",
        "One guest: just the name. Otherwise join all but the last with ', ' and add ' and ' + last.",
        "Return an f-string: f'{host} invites {guest_text} to the party!'.",
    ],
    hints_ru=[
        "Сначала собери полный список гостей: guests = [name, *friends] или [name] + list(friends).",
        "Один гость – просто имя. Иначе соедини всех, кроме последнего, через ', ' и добавь ' and ' + последний.",
        "Верни f-строку: f'{host} invites {guest_text} to the party!'.",
    ],
    explanation_en=("*friends swallows any number of extra guests; host stays a keyword-only argument because it comes "
                    "after *friends, so a caller can never pass it by position by accident. "
                    "Joining all-but-last with ', ' and appending ' and last' handles 2, 3 and 10 guests with the same code."),
    explanation_ru=("*friends забирает любое число гостей; host становится только-именованным, потому что стоит после *friends, "
                    "и его нельзя случайно передать позиционно. Соединение всех, кроме последнего, через ', ' плюс ' and последний' "
                    "одинаково работает для 2, 3 и 10 гостей."),
    talk_track=[
        "Point out that host after *friends is keyword-only by construction.",
        "Walk through the three guest-count cases out loud before coding.",
        "Mention str.join avoids a trailing comma bug.",
    ],
    complexity="O(n) in the number of guests",
    followups=["How would you handle zero friends and an empty name?", "Make the word 'and' configurable for other languages."],
)

STARTER = '''
def invite(name, *friends, host="Pixel"):
    ...
'''

EXAMPLES = [
    {"call": "invite('Bob')", "expected": "'Pixel invites Bob to the party!'"},
    {"call": "invite('Bob', 'Ann')", "expected": "'Pixel invites Bob and Ann to the party!'"},
    {"call": "invite('Bob', 'Ann', 'Tom', host='Byte')", "expected": "'Byte invites Bob, Ann and Tom to the party!'"},
]

SOLUTION = '''
def invite(name, *friends, host="Pixel"):
    guests = [name, *friends]
    if len(guests) == 1:
        guest_text = guests[0]
    else:
        guest_text = ", ".join(guests[:-1]) + " and " + guests[-1]
    return f"{host} invites {guest_text} to the party!"
'''

TESTS = '''
def test_one_guest(ns, check):
    check(ns["invite"]("Bob"), "Pixel invites Bob to the party!", "invite('Bob')")

def test_two_guests(ns, check):
    check(ns["invite"]("Bob", "Ann"), "Pixel invites Bob and Ann to the party!", "invite('Bob', 'Ann')")

def test_three_guests_custom_host(ns, check):
    check(ns["invite"]("Bob", "Ann", "Tom", host="Byte"),
          "Byte invites Bob, Ann and Tom to the party!", "invite('Bob', 'Ann', 'Tom', host='Byte')")

def test_five_guests(ns, check):
    check(ns["invite"]("A", "B", "C", "D", "E"),
          "Pixel invites A, B, C, D and E to the party!", "invite('A', 'B', 'C', 'D', 'E')")

def test_host_is_keyword_only(ns, check, raises):
    import inspect
    params = inspect.signature(ns["invite"]).parameters
    check(params["host"].kind, inspect.Parameter.KEYWORD_ONLY, "host is keyword-only (defined after *friends)")
'''

LEVELS = dict(
    middle=dict(
        note_en=("Builds the guest list once and handles 'one' versus 'many' in a single if: it works and it is clear. "
                 "What is left on the table: the English list rule ('A, B and C') is buried inside invite, so it cannot "
                 "be reused for the next message or tested on its own, and the word 'and' is hard-coded, which is exactly "
                 "what the follow-up question asks about."),
        note_ru=("Список гостей собран один раз, «один или много» решает единственный if: работает и понятно. "
                 "Что осталось: правило английского перечисления («A, B and C») зарыто внутри invite, его не переиспользовать "
                 "в следующем сообщении и не проверить отдельно, а слово and прибито гвоздями – ровно об этом спрашивает "
                 "дополнительный вопрос."),
    ),
    senior=dict(
        code='''
def join_names(names, last_sep=" and "):
    """'A', 'A and B', 'A, B and C'."""
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + last_sep + names[-1]

def invite(name, *friends, host="Pixel"):
    return f"{host} invites {join_names([name, *friends])} to the party!"
''',
        note_en=("Two jobs, two functions: joining names in English is a small pure helper with a configurable last "
                 "separator and its own tests; invite only formats the sentence. The helper handles 0, 1 and n names, "
                 "so invite needs no special cases at all. host stays keyword-only after *friends, and a senior says "
                 "that out loud instead of hoping the interviewer notices."),
        note_ru=("Две работы – две функции: перечисление имён по-английски стало маленьким чистым помощником с настраиваемым "
                 "последним разделителем и своими тестами, а invite только форматирует предложение. Помощник обрабатывает "
                 "0, 1 и n имён, поэтому в invite особых случаев нет вовсе. host остаётся только-именованным после *friends, "
                 "и сеньор говорит это вслух, а не ждёт, пока интервьюер заметит."),
    ),
)
