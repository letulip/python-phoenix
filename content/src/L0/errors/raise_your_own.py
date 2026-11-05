META = dict(
    id="l0.errors.raise-your-own", type="retype", order=40,
    difficulty=1, minutes=3, world="bybit",
    concepts=["raise", "value-error", "early-return"],
    story_en="Dr. Candle tried to withdraw minus forty dollars 'as an experiment'. The function now has boundaries.",
    title="Raise your own",
    statement_en="Retype the function: two guard clauses that raise ValueError with precise messages, then the normal path.",
    hints_en=["raise ValueError('message') stops the function immediately; put the guards before the real work."],
    hints_ru=["raise ValueError('сообщение') немедленно останавливает функцию; ставь проверки до основной работы."],
    explanation_en="Guard clauses at the top fail fast with a message the caller can show. ValueError is the conventional class for 'right type, wrong value'.",
    explanation_ru="Проверки в начале быстро падают с сообщением, которое можно показать вызывающему. ValueError – принятый класс для «тип верный, значение неверное».",
)

MODEL = '''
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount
'''

STARTER = ""

TESTS = '''
def test_normal(ns, check):
    check(ns["withdraw"](100, 30), 70, "withdraw(100, 30)")

def test_non_positive(ns, check, raises):
    err = raises(ValueError, ns["withdraw"], 100, 0)
    check(str(err), "amount must be positive", "message for amount 0")

def test_insufficient(ns, check, raises):
    err = raises(ValueError, ns["withdraw"], 10, 50)
    check(str(err), "insufficient funds", "message for overdraft")
'''
