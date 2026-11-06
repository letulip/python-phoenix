META = dict(
    id="l0.comprehensions.top-shorts", type="task", order=70,
    difficulty=2, minutes=6, world="shorts",
    concepts=["list-comprehension", "comprehension-if", "sorted-key", "lambda"],
    story_en="Pixel's channel analytics: which Shorts actually worked? The 300-second 'short' is disqualified. Pixel is bitter about it.",
    title="Top Shorts",
    statement_en=("Write top_shorts(videos, min_views) -> list[str]. videos is a list of dicts with keys 'title', 'views' and "
                  "'seconds'. Return the titles of videos that are 60 seconds or shorter and have at least min_views views, "
                  "ordered by views descending; equal views keep their original order."),
    hints_en=[
        "Filter first with a comprehension: v['seconds'] <= 60 and v['views'] >= min_views.",
        "Sort by views descending: key=lambda v: v['views'], reverse=True, or key=lambda v: -v['views'].",
        "Finally map to titles with another comprehension.",
    ],
    hints_ru=[
        "Сначала отфильтруй включением: v['seconds'] <= 60 and v['views'] >= min_views.",
        "Отсортируй по просмотрам по убыванию: key=lambda v: v['views'], reverse=True, или key=lambda v: -v['views'].",
        "В конце вытащи заголовки ещё одним включением.",
    ],
    explanation_en=("Filter, sort, project: three small steps read better than one clever line. Python's sort is stable, "
                    "so equal views keep their original order even with reverse=True."),
    explanation_ru=("Отфильтровать, отсортировать, спроецировать: три маленьких шага читаются лучше одной хитрой строки. "
                    "Сортировка в Python устойчива, поэтому равные просмотры сохраняют исходный порядок даже с reverse=True."),
    talk_track=[
        "Say filter, then sort, then project: three small steps beat one clever line.",
        "Mention Python's sort is stable, so equal views keep their order even with reverse=True.",
    ],
    complexity="O(n log n)",
    followups=["How would you add a secondary order by title?", "What if views is missing for some videos?"],
)

STARTER = '''
def top_shorts(videos, min_views):
    ...
'''

EXAMPLES = [
    {"call": "top_shorts([{'title': 'Lake', 'views': 900, 'seconds': 45}, {'title': 'Long one', 'views': 5000, 'seconds': 300}, {'title': 'Sunrise', 'views': 1200, 'seconds': 58}], 500)",
     "expected": "['Sunrise', 'Lake']"},
]

SOLUTION = '''
def top_shorts(videos, min_views):
    shorts = [v for v in videos if v["seconds"] <= 60 and v["views"] >= min_views]
    shorts.sort(key=lambda v: v["views"], reverse=True)
    return [v["title"] for v in shorts]
'''

TESTS = '''
VIDEOS = [
    {"title": "Lake", "views": 900, "seconds": 45},
    {"title": "Long one", "views": 5000, "seconds": 300},
    {"title": "Sunrise", "views": 1200, "seconds": 58},
    {"title": "Quiet", "views": 100, "seconds": 20},
]

def test_filter_and_order(ns, check):
    check(ns["top_shorts"](VIDEOS, 500), ["Sunrise", "Lake"], "top_shorts(VIDEOS, 500)")

def test_equal_views_keep_order(ns, check):
    vids = [{"title": "A", "views": 100, "seconds": 30}, {"title": "B", "views": 100, "seconds": 20}, {"title": "C", "views": 300, "seconds": 10}]
    check(ns["top_shorts"](vids, 0), ["C", "A", "B"], "stable among equal views")

def test_none_qualify(ns, check):
    check(ns["top_shorts"](VIDEOS, 10000), [], "nothing reaches 10000 views")

def test_exact_limits(ns, check):
    vids = [{"title": "Edge", "views": 500, "seconds": 60}]
    check(ns["top_shorts"](vids, 500), ["Edge"], "60 seconds and exactly min_views qualify")

def test_input_untouched(ns, check):
    before = [dict(v) for v in VIDEOS]
    ns["top_shorts"](VIDEOS, 0)
    check(VIDEOS, before, "videos list not reordered")
'''

LEVELS = dict(
    middle=dict(
        code='''
def top_shorts(videos, min_views):
    shorts = []
    for v in videos:
        if v["seconds"] <= 60:
            if v["views"] >= min_views:
                shorts.append(v)
    shorts.sort(key=lambda v: v["views"], reverse=True)
    titles = []
    for v in shorts:
        titles.append(v["title"])
    return titles
''',
        note_en=("Filter, sort, project, in that order: correct, and the stability of sort is used, perhaps without "
                 "knowing it. The nested ifs are one 'and', the two append loops are two comprehensions, and the magic "
                 "60 has no name. Each is a small reviewer comment; together they say 'knows the algorithm, not yet the "
                 "language'."),
        note_ru=("Отфильтровать, отсортировать, спроецировать, именно в таком порядке: верно, и устойчивость сортировки "
                 "использована, пусть и неосознанно. Вложенные if – это один and, два цикла с append – два включения, а у "
                 "магического 60 нет имени. Каждое – мелкое замечание ревьюера; вместе они говорят «знает алгоритм, но "
                 "ещё не язык»."),
    ),
    senior=dict(
        code='''
MAX_SHORT_SECONDS = 60

def top_shorts(videos, min_views):
    """Titles of qualifying Shorts, most viewed first; equal views keep input order."""
    def qualifies(video):
        return video["seconds"] <= MAX_SHORT_SECONDS and video["views"] >= min_views
    ranked = sorted((v for v in videos if qualifies(v)), key=lambda v: v["views"], reverse=True)
    return [v["title"] for v in ranked]
''',
        note_en=("Names the rule and the constant, so the filter reads as a sentence, and sorted over a generator never "
                 "materialises the intermediate list. A senior says out loud that Python's sort is stable, so reverse=True "
                 "keeps equal views in input order, and that (-views, title) would be the key the moment a tie-break is "
                 "requested. Then stops."),
        note_ru=("Правило и константа названы, поэтому фильтр читается как предложение, а sorted по генератору не "
                 "материализует промежуточный список. Сеньор вслух говорит, что сортировка в Python устойчива, поэтому "
                 "reverse=True сохраняет порядок равных просмотров, и что (-views, title) станет ключом, как только "
                 "попросят разрешать ничьи. И останавливается."),
    ),
)
