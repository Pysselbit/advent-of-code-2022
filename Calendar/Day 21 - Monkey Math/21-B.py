ROOT = "root"
TARGET = "humn"

ADD = "+"
SUBTRACT = "-"
MULTIPLY = "*"
DIVIDE = "/"

INPUT_ID = 0
INPUT_N = 1
INPUT_A = 1
INPUT_B = 3
INPUT_OPERATION = 2


# Monkey with either a number or an operation.
class Monkey:
    def __init__(self, id):
        self.id = id
        self.n = None
        self.a = self.b = self.operation = None
        self.has_number = self.has_operation = False

    def set_number(self, n):
        self.n = n
        self.has_number = True

    def set_operation(self, a, b, operation):
        self.a = a
        self.b = b
        self.operation = operation
        self.has_operation = True

    # Call out number.
    def call(self):
        if self.has_number:
            return self.n

        a = self.a.call()
        b = self.b.call()

        if self.operation == ADD:
            return a + b
        if self.operation == SUBTRACT:
            return a - b
        if self.operation == MULTIPLY:
            return a * b
        if self.operation == DIVIDE:
            return a // b


# Load input into monkey objects.
def load_input(path):
    monkeys = {}

    with open(path) as file:
        lines = [line.strip().split(" ") for line in file]

        # Set monkeys:
        for line in lines:
            monkey = Monkey(line[INPUT_ID][0:4])
            monkeys[monkey.id] = monkey

        # Set numbers or operations:
        for line in lines:
            if line[INPUT_N].isdigit():
                monkeys[line[INPUT_ID][0:4]].set_number(int(line[INPUT_N]))
            else:
                monkeys[line[INPUT_ID][0:4]].set_operation(monkeys[line[INPUT_A]], monkeys[line[INPUT_B]],
                                                           line[INPUT_OPERATION])

    return monkeys


# Get step-by-step path from monkey a to monkey b.
def get_path(a, b, path):
    if a == b:
        path.insert(0, a)
        return True

    if a.has_number:
        return False

    if get_path(a.a, b, path) or get_path(a.b, b, path):
        path.insert(0, a)
        return True

    return False


# Get the number that the monkey at the end of the path has to have for root.a to equal root.b.
def get_target_number(root, path):
    # Get the number we want to reach:
    n = root.a.call() if root.b in path else root.b.call()

    # Iterate over path, reversing all operations:
    for i in range(1, len(path) - 1):
        monkey = path[i]
        operation = monkey.operation

        if monkey.a in path:
            b = monkey.b.call()

            if operation == ADD:
                n = n - b
            elif operation == SUBTRACT:
                n = n + b
            elif operation == MULTIPLY:
                n = n // b
            elif operation == DIVIDE:
                n = n * b

        elif monkey.b in path:
            a = monkey.a.call()

            if operation == ADD:
                n = n - a
            elif operation == SUBTRACT:
                n = a - n
            elif operation == MULTIPLY:
                n = n // a
            elif operation == DIVIDE:
                n = a // n

    return n


monkeys = load_input("input.txt")

path = []
get_path(monkeys[ROOT], monkeys[TARGET], path)

print(get_target_number(monkeys[ROOT], path))
