META = dict(
    id="l0.strings.secret-shift", type="cloze", order=30,
    difficulty=2, minutes=3, world="everyday",
    concepts=["ord-chr"],
    story_en="Ada's recipe book shifts every letter so the seagulls can't read it. The seagulls have not cracked it yet.",
    title="Secret shift",
    statement_en=("Fill in the blanks so shift_letter moves a lowercase letter k places along the alphabet and wraps "
                  "around: shift_letter('z', 1) is 'a' and shift_letter('c', -3) is 'z'."),
    hints_en=["ord turns a character into its number; the alphabet has 26 letters, and % keeps the result inside it, even for negative k."],
    hints_ru=["ord превращает символ в число; в алфавите 26 букв, а % удерживает результат внутри него даже при отрицательном k."],
    explanation_en="Subtracting ord('a') maps a..z to 0..25, the modulo wraps in both directions, and adding the base back gives a code point that chr turns into the letter.",
    explanation_ru="Вычитание ord('a') переводит a..z в 0..25, остаток от деления замыкает круг в обе стороны, а прибавление базы обратно даёт код, который chr превращает в букву.",
)

STARTER = '''
def shift_letter(ch, k):
    """Shift a lowercase letter by k places, wrapping from z back to a."""
    base = ord("a")
    return chr((___(ch) - base + k) % ___ + base)

# shift_letter("a", 1) -> "b",  shift_letter("z", 1) -> "a",  shift_letter("c", -3) -> "z"
'''

SOLUTION = '''
def shift_letter(ch, k):
    """Shift a lowercase letter by k places, wrapping from z back to a."""
    base = ord("a")
    return chr((ord(ch) - base + k) % 26 + base)
'''

TESTS = '''
def test_simple(ns, check):
    check(ns["shift_letter"]("a", 1), "b", "shift_letter('a', 1)")

def test_wrap_forward(ns, check):
    check(ns["shift_letter"]("z", 1), "a", "shift_letter('z', 1)")

def test_wrap_backward(ns, check):
    check(ns["shift_letter"]("c", -3), "z", "shift_letter('c', -3)")

def test_rot13(ns, check):
    check(ns["shift_letter"]("m", 13), "z", "shift_letter('m', 13)")
'''
