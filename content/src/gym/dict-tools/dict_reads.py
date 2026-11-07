META = dict(
    id="gym.dict-tools.dict-reads", type="predict", order=50,
    difficulty=2, minutes=2, world="game",
    concepts=["dict-get", "setdefault", "dict-basics"],
    title="Read get and setdefault",
    statement_en="Write what this code prints, one line per print. The last line is a sorted list of (key, value) tuples.",
    hints_en=["get never adds a key; setdefault adds it and returns the stored value; the third line creates or increments."],
    hints_ru=["get никогда не добавляет ключ; setdefault добавляет и возвращает сохранённое значение; третья строка создаёт или увеличивает."],
    explanation_en="get is a question, setdefault is a question with a side effect. Knowing which one touched the dict is what the last print checks.",
    explanation_ru="get – вопрос, setdefault – вопрос с побочным эффектом. Последний print проверяет именно то, понимаешь ли ты, кто из них тронул словарь.",
)

VARIANTS = [
    dict(STOCK="{'potion': 3, 'arrow': 20}", MISSING="shield", NEW="rope", KEY="arrow", ADD="5"),
    dict(STOCK="{'gem': 1}", MISSING="coal", NEW="stick", KEY="coal", ADD="2"),
    dict(STOCK="{'torch': 4, 'map': 1}", MISSING="rope", NEW="map", KEY="torch", ADD="1"),
]

SNIPPET = '''
stock = @STOCK@
print(stock.get("@MISSING@", 0))
print(stock.setdefault("@NEW@", []))
stock["@KEY@"] = stock.get("@KEY@", 0) + @ADD@
print(sorted(stock.items()))
'''
