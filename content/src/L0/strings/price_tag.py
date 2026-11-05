META = dict(
    id="l0.strings.price-tag", type="cloze", order=20,
    difficulty=2, minutes=3, world="everyday",
    concepts=["f-string", "format-spec"],
    story_en="Ada's price tags must line up on the shelf. Crooked tags, she says, make bread taste suspicious.",
    title="Price tag",
    statement_en=("Fill in the two format specs: the name left-aligned in a field of 10 characters, the price right-aligned "
                  "in a field of 6 characters with exactly two decimals. price_tag('rye', 2.5) is 'rye         2.50'."),
    hints_en=["A spec starts with a colon: {name:<10} pads to 10 on the right, {price:>6.2f} pads to 6 on the left with 2 decimals."],
    hints_ru=["Спецификатор начинается с двоеточия: {name:<10} дополняет до 10 справа, {price:>6.2f} дополняет до 6 слева с двумя знаками."],
    explanation_en="Format specs replace manual padding with spaces and str(round(...)). The f after the precision means fixed-point, so 12 becomes 12.00 and 2.5 becomes 2.50.",
    explanation_ru="Спецификаторы формата заменяют ручное дополнение пробелами и str(round(...)). f после точности означает фиксированную запятую, поэтому 12 становится 12.00, а 2.5 – 2.50.",
)

STARTER = '''
def price_tag(name, price):
    # name left-aligned in 10 characters, price right-aligned in 6 with 2 decimals
    return f"{name___}{price___}"

# price_tag("rye", 2.5) -> "rye         2.50"
'''

SOLUTION = '''
def price_tag(name, price):
    return f"{name:<10}{price:>6.2f}"
'''

TESTS = '''
def test_rye(ns, check):
    check(ns["price_tag"]("rye", 2.5), "rye         2.50", "price_tag('rye', 2.5)")

def test_croissant(ns, check):
    check(ns["price_tag"]("croissant", 12), "croissant  12.00", "price_tag('croissant', 12)")

def test_width(ns, check):
    check(len(ns["price_tag"]("a", 0.5)), 16, "total width is 16")

def test_two_decimals(ns, check):
    check(ns["price_tag"]("bagel", 1.999).endswith("2.00"), True, "1.999 rounds to 2.00")
'''
