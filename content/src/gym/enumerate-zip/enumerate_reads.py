META = dict(
    id="gym.enumerate-zip.enumerate-reads", type="predict", order=30,
    difficulty=1, minutes=1, world="neutral",
    concepts=["enumerate", "zip"],
    title="Read enumerate and zip",
    statement_en="Write what this code prints. The last line is a list of tuples; mind how many pairs zip produces.",
    hints_en=["enumerate yields (number, item) starting at start; zip stops at the shorter input."],
    hints_ru=["enumerate выдаёт (номер, элемент), начиная со start; zip останавливается на более коротком входе."],
    explanation_en="Two facts to keep in the hands: enumerate's start shifts only the number, and zip silently truncates to the shortest input, which strict=True turns into an error.",
    explanation_ru="Два факта, которые должны жить в руках: start у enumerate сдвигает только номер, а zip молча усекает до самого короткого входа, и strict=True превращает это в ошибку.",
)

VARIANTS = [
    dict(NAMES="['ann', 'bob', 'cid']", START="1", NUMS="[10, 20]"),
    dict(NAMES="['rope', 'lamp']", START="0", NUMS="[3, 12, 7]"),
    dict(NAMES="['x', 'y', 'z']", START="5", NUMS="[1]"),
]

SNIPPET = '''
names = @NAMES@
for number, name in enumerate(names, start=@START@):
    print(number, name)
print(list(zip(names, @NUMS@)))
'''
