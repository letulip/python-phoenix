META = dict(
    id="gym.join.join-shapes", type="retype", order=50,
    difficulty=1, minutes=2, world="neutral",
    concepts=["split-join", "f-string", "str-case"],
    title="Four shapes of join",
    statement_en="Retype the snippet: a space join, a comma join, a newline join over an f-string generator, and an empty join of first letters.",
    hints_en=["Every line is separator.join(iterable); the generator inside the last two needs no extra brackets."],
    hints_ru=["Каждая строка – separator.join(iterable); генератору внутри последних двух лишние скобки не нужны."],
    explanation_en="These four shapes cover almost every string you will ever assemble: sentence, CSV, multi-line block, acronym. The hands need to know them without thinking.",
    explanation_ru="Эти четыре формы закрывают почти любую строку, которую придётся собирать: предложение, CSV, многострочный блок, аббревиатура. Руки должны знать их не думая.",
)

VARIANTS = [
    dict(WORDS="['one', 'two', 'three']", SENTENCE="one two three", CSV="one,two,three", INITIALS="OTT"),
    dict(WORDS="['game', 'set', 'match']", SENTENCE="game set match", CSV="game,set,match", INITIALS="GSM"),
    dict(WORDS="['pixel', 'byte']", SENTENCE="pixel byte", CSV="pixel,byte", INITIALS="PB"),
]

MODEL = '''
words = @WORDS@
sentence = " ".join(words)
csv = ",".join(words)
lines = "\\n".join(f"- {w}" for w in words)
initials = "".join(w[0].upper() for w in words)
'''

STARTER = ""

TESTS = '''
def test_sentence_and_csv(ns, check):
    check((ns["sentence"], ns["csv"]), ("@SENTENCE@", "@CSV@"), "sentence, csv")

def test_lines(ns, check):
    check(ns["lines"], "\\n".join("- " + w for w in @WORDS@), "lines")

def test_initials(ns, check):
    check(ns["initials"], "@INITIALS@", "initials")
'''
