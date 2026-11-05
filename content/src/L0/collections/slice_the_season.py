META = dict(
    id="l0.collections.slice-the-season", type="cloze", order=50,
    difficulty=2, minutes=3, world="tennis",
    concepts=["slicing"],
    story_en="Coach Topspin wants the last three results, then every second one, then everything backwards. Coaches are like that.",
    title="Slice the season",
    statement_en="Fill in the three slices. Each blank is the part inside the square brackets.",
    hints_en=["Slices are start:stop:step. A negative start counts from the end, a step of 2 skips every other item, a step of -1 walks backwards."],
    hints_ru=["Срез – это start:stop:step. Отрицательный start считает с конца, шаг 2 пропускает каждый второй, шаг -1 идёт назад."],
    explanation_en="scores[-3:] is 'from the third-to-last to the end', scores[::2] is 'every second item', scores[::-1] is the reversed copy. Slicing never raises and always returns a new list.",
    explanation_ru="scores[-3:] – «с третьего с конца до конца», scores[::2] – «каждый второй», scores[::-1] – перевёрнутая копия. Срез никогда не падает и всегда возвращает новый список.",
)

STARTER = '''
scores = [10, 25, 7, 31, 18, 22]
last_three = scores[___]        # [31, 18, 22]
every_second = scores[___]      # [10, 7, 18]
backwards = scores[___]         # [22, 18, 31, 7, 25, 10]
'''

SOLUTION = '''
scores = [10, 25, 7, 31, 18, 22]
last_three = scores[-3:]
every_second = scores[::2]
backwards = scores[::-1]
'''

TESTS = '''
def test_last_three(ns, check):
    check(ns["last_three"], [31, 18, 22], "last_three")

def test_every_second(ns, check):
    check(ns["every_second"], [10, 7, 18], "every_second")

def test_backwards(ns, check):
    check(ns["backwards"], [22, 18, 31, 7, 25, 10], "backwards")

def test_original_untouched(ns, check):
    check(ns["scores"], [10, 25, 7, 31, 18, 22], "scores unchanged")
'''
