import re

N_ROUNDS = 10000

INDEX_MONKEY_ID = 0
INDEX_ITEMS = 1
INDEX_OPERATION = 2
INDEX_TEST = 3
INDEX_PASS_NEXT = 4
INDEX_FAIL_NEXT = 5
INPUT_ENTRY_LENGTH = 7

ITEMS = "items"
OPERATION = "operation"
OPERATION_NUMBER = "operation_number"
TEST = "test"
PASS_NEXT = "pass_next"
FAIL_NEXT = "fail_next"
INSPECTION_COUNT = "inspection_count"

OPERATION_ADD = "+"
OPERATION_MULTIPLY = "*"
OPERATION_NUMBER_OLD = "old"

monkeys = []

# Worry levels grow very fast. By each turn calculating the worry level modulo this divisor it stays manageable.
# This divisor is the product of all the monkeys' test divisors, which keeps the divisibility in order.
divisor = 1


# Load and parse input.
def load_input(path):
    file = open(path)
    lines = file.readlines()
    file.close()

    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()

    # Parse input and store in monkey objects:
    for i in range(0, len(lines) // INPUT_ENTRY_LENGTH + 1):
        index = i * INPUT_ENTRY_LENGTH

        items = list(map(int, re.findall(r'\d+', lines[index + INDEX_ITEMS])))
        if lines[index + INDEX_OPERATION].find(OPERATION_ADD) > 0:
            operation = OPERATION_ADD
        else:
            operation = OPERATION_MULTIPLY
        operation_number = re.search(r'\d+', lines[index + INDEX_OPERATION])
        if operation_number == None:
            operation_number = OPERATION_NUMBER_OLD
        else:
            operation_number = int(operation_number.group())
        test = int(re.search(r'\d+', lines[index + INDEX_TEST]).group())
        pass_next = int(re.search(r'\d+', lines[index + INDEX_PASS_NEXT]).group())
        fail_next = int(re.search(r'\d+', lines[index + INDEX_FAIL_NEXT]).group())

        monkeys.append({
            ITEMS: items,
            OPERATION: operation,
            OPERATION_NUMBER: operation_number,
            TEST: test,
            PASS_NEXT: pass_next,
            FAIL_NEXT: fail_next,
            INSPECTION_COUNT: 0
        })

        # Multiply test divisor:
        global divisor
        divisor *= test


# Run turn for specified monkey (in which it inspects and throws all its items).
def run_turn(monkey):
    while len(monkey[ITEMS]) > 0:
        worry_level = monkey[ITEMS].pop(0)

        if monkey[OPERATION_NUMBER] == OPERATION_NUMBER_OLD:
            operation_number = worry_level
        else:
            operation_number = monkey[OPERATION_NUMBER]

        if monkey[OPERATION] == OPERATION_ADD:
            worry_level += operation_number
        else:
            worry_level *= operation_number

        # Keep worry level manageable while maintaining divisibility:
        worry_level %= divisor

        # Test worry level (divisibility) to find receiving monkey:
        if worry_level % monkey[TEST] == 0:
            next_monkey = monkey[PASS_NEXT]
        else:
            next_monkey = monkey[FAIL_NEXT]

        # Throw item to receiver and increase inspection count:
        monkeys[next_monkey][ITEMS].append(worry_level)
        monkey[INSPECTION_COUNT] += 1


# Run one turn for each monkey.
def run_round():
    for monkey in monkeys:
        run_turn(monkey)


load_input("input.txt")

# Run all rounds:
for i in range(0, N_ROUNDS):
    run_round()

# Find monkeys with the highest inspection count:
inspection_max_a = inspection_max_b = 0
for monkey in monkeys:
    inspection_count = monkey[INSPECTION_COUNT]

    if inspection_count > inspection_max_a:
        inspection_max_a, inspection_max_b = inspection_count, inspection_max_a
    elif inspection_count > inspection_max_b:
        inspection_max_b = inspection_count

print(inspection_max_a * inspection_max_b)
