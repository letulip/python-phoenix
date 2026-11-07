META = dict(
    id="gym.unpacking.star-call", type="cloze", order=50,
    difficulty=1, minutes=1, world="everyday",
    concepts=["star-args", "tuple-unpacking"],
    title="Spread a list into arguments",
    statement_en="Fill in the two blanks: print the parts as separate arguments, then pass the values to total as separate arguments. Both blanks are the same single character.",
    hints_en=["A star before a list in a call spreads it: print(*parts) and total(*values)."],
    hints_ru=["Звёздочка перед списком в вызове раскрывает его: print(*parts) и total(*values)."],
    explanation_en="The star in a call is the mirror of *args in a def: it turns a list into separate arguments, so print gets its sep between them and total receives them one by one.",
    explanation_ru="Звёздочка в вызове – зеркало *args в def: она превращает список в отдельные аргументы, так что print ставит sep между ними, а total получает их по одному.",
)

VARIANTS = [
    dict(PARTS="['rope', 'lamp', 'map']", SEP=", ", PRINTED="rope, lamp, map", VALUES="[1, 2, 3]", RESULT="6"),
    dict(PARTS="['game', 'set', 'match']", SEP=" - ", PRINTED="game - set - match", VALUES="[10, 20]", RESULT="30"),
    dict(PARTS="['a', 'b']", SEP="/", PRINTED="a/b", VALUES="[5]", RESULT="5"),
]

STARTER = '''
parts = @PARTS@
print(___parts, sep="@SEP@")          # prints: @PRINTED@

def total(*numbers):
    return sum(numbers)

values = @VALUES@
result = total(___values)            # @RESULT@
'''

SOLUTION = '''
parts = @PARTS@
print(*parts, sep="@SEP@")

def total(*numbers):
    return sum(numbers)

values = @VALUES@
result = total(*values)
'''

TESTS = '''
def test_printed(stdout, check):
    check(stdout.strip(), "@PRINTED@", "printed line")

def test_result(ns, check):
    check(ns["result"], @RESULT@, "result")

def test_star_in_calls(src, ast_tools, check):
    check(ast_tools.count_nodes(src, "Starred") >= 2, True, "both calls spread a list with *")
'''
