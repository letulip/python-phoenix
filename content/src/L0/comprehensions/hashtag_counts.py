META = dict(
    id="l0.comprehensions.hashtag-counts", type="task", order=64,
    difficulty=2, minutes=6, world="shorts",
    concepts=["list-comprehension", "comprehension-if", "dict-basics"],
    story_en="Pixel tags every Short with #lake, #Lake or #LAKE depending on mood. The analytics machine would like one number per tag and one mood per cat.",
    title="Count the hashtags",
    statement_en=("Write hashtag_counts(captions) -> dict. captions is a list of strings; a hashtag is a word (split on "
                  "whitespace) that starts with '#'. Return a dict of hashtag -> number of appearances across all "
                  "captions, comparing hashtags in lowercase: '#Lake' and '#lake' are one tag with the key '#lake'. "
                  "Keys appear in order of first appearance. No hashtags gives {}. Use at least one comprehension."),
    hints_en=[
        "Collect the tags first: [word.lower() for caption in captions for word in caption.split() if word.startswith('#')].",
        "Then count: counts[tag] = counts.get(tag, 0) + 1 for every tag.",
        "The nested comprehension reads like nested loops: outer first, inner second.",
    ],
    hints_ru=[
        "Сначала собери теги: [word.lower() for caption in captions for word in caption.split() if word.startswith('#')].",
        "Потом сосчитай: counts[tag] = counts.get(tag, 0) + 1 для каждого тега.",
        "Вложенное включение читается как вложенные циклы: сначала внешний, потом внутренний.",
    ],
    explanation_en=("A comprehension with two for clauses flattens 'words of every caption' into one list, and the if "
                    "keeps only hashtags. Counting with dict.get(tag, 0) + 1 is the smallest correct tally; "
                    "collections.Counter is the same idea with a name."),
    explanation_ru=("Включение с двумя for разворачивает «слова каждой подписи» в один список, а if оставляет только "
                    "хэштеги. Подсчёт через dict.get(tag, 0) + 1 – самый маленький верный счётчик; collections.Counter – "
                    "та же идея, но с именем."),
    talk_track=[
        "Say the nested comprehension flattens captions into words and the if keeps hashtags.",
        "Mention Counter does the counting and why you did or did not use it.",
        "Complexity O(total words).",
    ],
    complexity="O(n) in the total number of words",
    followups=["How would '#lake,' with a trailing comma be counted?", "Return the top three tags instead of all of them."],
)

STARTER = '''
def hashtag_counts(captions):
    ...
'''

EXAMPLES = [
    {"call": "hashtag_counts(['Lake #sunrise #Lake', '#lake again'])", "expected": "{'#sunrise': 1, '#lake': 2}"},
    {"call": "hashtag_counts(['no tags here'])", "expected": "{}"},
]

SOLUTION = '''
def hashtag_counts(captions):
    tags = [word.lower() for caption in captions for word in caption.split() if word.startswith("#")]
    counts = {}
    for tag in tags:
        counts[tag] = counts.get(tag, 0) + 1
    return counts
'''

TESTS = '''
def test_mixed_case(ns, check):
    check(ns["hashtag_counts"](["Lake #sunrise #Lake", "#lake again"]), {"#sunrise": 1, "#lake": 2}, "hashtag_counts(['Lake #sunrise #Lake', '#lake again'])")

def test_no_tags(ns, check):
    check((ns["hashtag_counts"](["no tags here"]), ns["hashtag_counts"]([])), ({}, {}), "no hashtags and no captions")

def test_hash_inside_a_word_is_not_a_tag(ns, check):
    check(ns["hashtag_counts"](["c#sharp #csharp"]), {"#csharp": 1}, "only words starting with # count")

def test_order_of_first_appearance(ns, check):
    check(list(ns["hashtag_counts"](["#b #a", "#a #c"])), ["#b", "#a", "#c"], "keys in order of first appearance")

def test_uses_comprehension(src, ast_tools, check):
    check(ast_tools.has_comprehension(src), True, "a comprehension is used")
'''

LEVELS = dict(
    middle=dict(
        code='''
def hashtag_counts(captions):
    tags = [word.lower() for caption in captions for word in caption.split() if word.startswith("#")]
    counts = {}
    for tag in tags:
        if tag in counts:
            counts[tag] += 1
        else:
            counts[tag] = 1
    return counts
''',
        note_en=("The nested comprehension pulls the tags out in one readable line, which is the hard part. The counting "
                 "loop is the if/else dance that dict.get(tag, 0) + 1 replaces, and a reviewer will say the word Counter "
                 "within seconds; have it ready before they do."),
        note_ru=("Вложенное включение вытаскивает теги одной читаемой строкой, и это сложная часть. Цикл подсчёта – тот "
                 "самый танец if/else, который заменяет dict.get(tag, 0) + 1, и ревьюер произнесёт слово Counter за "
                 "считанные секунды; приготовь его раньше."),
    ),
    senior=dict(
        code='''
from collections import Counter

def hashtag_counts(captions):
    """How often each hashtag (lowercased) appears across the captions."""
    tags = (word.casefold() for caption in captions for word in caption.split() if word.startswith("#"))
    return dict(Counter(tags))
''',
        note_en=("Extraction stays a comprehension, a generator since it is consumed once, and counting is delegated to "
                 "collections.Counter, the standard answer to 'how many of each'. casefold rather than lower for the "
                 "comparison. A senior converts back to a plain dict because the signature promised one, and says a "
                 "regex is needed the moment '#lake,' with punctuation must count."),
        note_ru=("Извлечение остаётся включением, причём генератором, раз оно потребляется один раз, а подсчёт отдан "
                 "collections.Counter – стандартному ответу на «сколько каждого». Для сравнения casefold, а не lower. "
                 "Сеньор превращает результат обратно в обычный dict, потому что сигнатура обещала его, и говорит, что "
                 "понадобится регулярное выражение, как только '#lake,' со знаком препинания должен засчитываться."),
    ),
)
