MODULE = dict(
    id="l0.errors", level=0, order=6,
    title_en="Errors and lookups", title_ru="Ошибки и безопасный поиск",
    concepts=["try-except", "except-else-finally", "raise", "value-error", "key-error", "index-error",
              "dict-get", "setdefault", "eafp-lbyl"],
    diagnostic=["l0.errors.robust-average"],
    chapter_en="Act I · Chapter 6: The lifeboats", chapter_ru="Акт I · Глава 6: Спасательные шлюпки",
    story_en=("Dr. Candle's trading bot reads prices from a feed that sometimes sends 'n/a' instead of a number, and the "
              "bot sinks every time. Captain Byte, who has strong opinions about sinking, demands lifeboats: code that "
              "expects trouble, catches it and keeps the ship afloat."),
    story_ru=("Торговый бот доктора Кэндл читает цены из ленты, которая иногда присылает «n/a» вместо числа, и бот тонет "
              "каждый раз. Капитан Байт, у которого твёрдое мнение о потоплениях, требует спасательные шлюпки: код, который "
              "ждёт беды, ловит её и держит корабль на плаву."),
    story_done_en="The bot survives bad data, the lifeboats are stowed and Pixel flips the studio sign to OPEN. Act I is over: the studio runs. Act II brings the first paying clients, and the toolbox you rebuilt gets heavier.",
    story_done_ru="Бот переживает плохие данные, шлюпки убраны, Пиксель переворачивает табличку на OPEN. Акт I окончен: студия работает. Акт II приведёт первых платящих клиентов, а ящик с инструментами, который ты восстановил, станет тяжелее.",
    card=dict(
        intro_en=("Exceptions are how Python says 'this did not work'. Catch the specific ones you expect with try/except, "
                  "raise your own when input is wrong, and prefer asking a dict politely (.get, setdefault) to crashing on "
                  "a missing key. Catch narrowly: a bare except hides bugs."),
        intro_ru=("Исключения – способ Python сказать «не получилось». Конкретные ожидаемые лови через try/except, свои "
                  "бросай через raise при неверном входе, а у словаря спрашивай вежливо (.get, setdefault), вместо того "
                  "чтобы падать на отсутствующем ключе. Лови узко: голый except прячет баги."),
        snippets=[
            dict(title_en="try / except a specific error", title_ru="try / except конкретной ошибки",
                 code='def parse_price(text):\n    try:\n        return float(text)\n    except ValueError:\n        return None          # "n/a" -> None instead of a crash\n',
                 note_en="Name the exception you expect. 'except Exception' only as a last resort, and never a bare 'except:'.",
                 note_ru="Называй исключение, которое ждёшь. except Exception – только как последняя мера, а голый except: – никогда."),
            dict(title_en="else and finally", title_ru="else и finally",
                 code='try:\n    value = risky()\nexcept KeyError as err:\n    log(f"missing {err}")\nelse:\n    use(value)               # only when nothing was raised\nfinally:\n    cleanup()                # always, even after a return\n',
                 note_en="else keeps the happy path out of the try block; finally is for releasing resources.",
                 note_ru="else выносит счастливый путь из блока try; finally – для освобождения ресурсов."),
            dict(title_en="raise your own", title_ru="бросай свои",
                 code='def withdraw(balance, amount):\n    if amount <= 0:\n        raise ValueError("amount must be positive")\n    return balance - amount\n',
                 note_en="Raise early with a precise message: ValueError for bad values, TypeError for wrong types, KeyError and IndexError for lookups.",
                 note_ru="Бросай рано и с точным сообщением: ValueError для плохих значений, TypeError для неверных типов, KeyError и IndexError для поиска."),
            dict(title_en="Polite dict lookups", title_ru="Вежливый поиск в словаре",
                 code='stock.get("coal", 0)                  # default instead of KeyError\ngroups.setdefault(key, []).append(x)  # create the list on first sight\nif key in stock:                      # look before you leap\n    ...\ntry:                                  # or ask forgiveness\n    value = stock[key]\nexcept KeyError:\n    value = 0\n',
                 note_en="Both styles are fine: try/except when the miss is rare, 'in' or .get when it is common.",
                 note_ru="Оба стиля хороши: try/except, когда промах редкий, in или .get, когда он частый."),
        ],
        gotchas_en=[
            "A bare except: also catches KeyboardInterrupt and typos like NameError; catch what you expect.",
            "A return inside try still runs finally, but skips else.",
            "KeyError, IndexError and ValueError are different classes: catching the wrong one catches nothing.",
        ],
        gotchas_ru=[
            "Голый except: ловит и KeyboardInterrupt, и опечатки вроде NameError; лови то, чего ждёшь.",
            "return внутри try всё равно выполняет finally, но пропускает else.",
            "KeyError, IndexError и ValueError – разные классы: поймав не тот, не поймаешь ничего.",
        ],
        phrase_en="I'll catch the specific exception here and let anything unexpected propagate.",
    ),
)
