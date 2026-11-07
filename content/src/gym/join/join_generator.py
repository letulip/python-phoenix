META = dict(
    id="gym.join.join-generator", type="cloze", order=40,
    difficulty=1, minutes=1, world="shorts",
    concepts=["split-join", "f-string"],
    title="Join a generator",
    statement_en="Fill in the separator so that the settings come out as 'key=value' pairs separated by a comma and a space, sorted by key.",
    hints_en=["The blank is the separator string: a comma followed by a space, in quotes."],
    hints_ru=["Пропуск – строка-разделитель: запятая и пробел, в кавычках."],
    explanation_en="join accepts a generator expression directly, so formatting and joining happen in one pass without a temporary list.",
    explanation_ru="join принимает генераторное выражение напрямую, поэтому форматирование и склейка идут за один проход без временного списка.",
)

VARIANTS = [
    dict(SETTINGS="{'res': '1080p', 'fps': 60}", LINE="fps=60, res=1080p"),
    dict(SETTINGS="{'mic': 'on', 'cam': 'off', 'bitrate': 6000}", LINE="bitrate=6000, cam=off, mic=on"),
    dict(SETTINGS="{'volume': 7}", LINE="volume=7"),
]

STARTER = '''
settings = @SETTINGS@
line = ___.join(f"{key}={value}" for key, value in sorted(settings.items()))
# line == "@LINE@"
'''

SOLUTION = '''
settings = @SETTINGS@
line = ", ".join(f"{key}={value}" for key, value in sorted(settings.items()))
'''

TESTS = '''
def test_line(ns, check):
    check(ns["line"], "@LINE@", "line")
'''
