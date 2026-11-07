META = dict(
    id="gym.comprehensions.comprehension-reads", type="predict", order=50,
    difficulty=2, minutes=2, world="neutral",
    concepts=["list-comprehension", "dict-comprehension", "sum", "any-all"],
    title="Read four comprehensions",
    statement_en="Write what this code prints, one line per print. The last print shows two values separated by a space.",
    hints_en=["'if n % 2' keeps odd numbers (1 is truthy); the dict comprehension maps n to n squared; any/all over a generator give booleans."],
    hints_ru=["if n % 2 оставляет нечётные (1 истинно); включение словаря отображает n в n в квадрате; any/all по генератору дают булевы значения."],
    explanation_en="Reading comprehensions is half of writing them: expression first, then the loop, then the filter. A bare 'if n % 2' relies on truthiness, which is why it reads as 'odd'.",
    explanation_ru="Читать включения – половина умения их писать: сначала выражение, потом цикл, потом фильтр. Голое if n % 2 опирается на истинность, поэтому читается как «нечётное».",
)

VARIANTS = [
    dict(NUMS="[1, 2, 3, 4, 5]", LIMIT="2"),
    dict(NUMS="[10, 15, 20, 25]", LIMIT="12"),
    dict(NUMS="[7, 8, 9]", LIMIT="100"),
]

SNIPPET = '''
nums = @NUMS@
print([n * 2 for n in nums if n % 2])
print({n: n ** 2 for n in nums[:3]})
print(sum(n for n in nums if n > @LIMIT@))
print(any(n > 100 for n in nums), all(n > 0 for n in nums))
'''
