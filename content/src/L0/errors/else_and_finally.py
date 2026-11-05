META = dict(
    id="l0.errors.else-and-finally", type="cloze", order=30,
    difficulty=2, minutes=3, world="neutral",
    concepts=["except-else-finally", "try-except"],
    story_en="Pixel logs everything. Especially the parts that worked. Especially the parts that always run.",
    title="else and finally",
    statement_en=("Fill in the two keywords: one block runs only when no exception happened, the other runs always, even "
                  "after a return. divide(6, 3) logs 'ok' then 'done'; divide(1, 0) logs 'division by zero' then 'done'."),
    hints_en=["The no-exception block is else; the always block is finally. Order in the code: try, except, else, finally."],
    hints_ru=["Блок без исключения – else; блок «всегда» – finally. Порядок в коде: try, except, else, finally."],
    explanation_en="else runs only on success and keeps the happy path out of the try body; finally runs on every exit, including return, which is why 'done' appears in both logs.",
    explanation_ru="else выполняется только при успехе и выносит счастливый путь из тела try; finally выполняется при любом выходе, включая return, поэтому 'done' есть в обоих журналах.",
)

STARTER = '''
log = []

def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        log.append("division by zero")
        return None
    ___:
        log.append("ok")
        return result
    ___:
        log.append("done")

# divide(6, 3) -> 2.0, log == ["ok", "done"]
# divide(1, 0) -> None, log gains ["division by zero", "done"]
'''

SOLUTION = '''
log = []

def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        log.append("division by zero")
        return None
    else:
        log.append("ok")
        return result
    finally:
        log.append("done")
'''

TESTS = '''
def test_success_then_failure(ns, check):
    ns["log"].clear()
    check(ns["divide"](6, 3), 2.0, "divide(6, 3)")
    check(list(ns["log"]), ["ok", "done"], "log after a successful division")
    check(ns["divide"](1, 0), None, "divide(1, 0)")
    check(list(ns["log"]), ["ok", "done", "division by zero", "done"], "log after dividing by zero")
'''
