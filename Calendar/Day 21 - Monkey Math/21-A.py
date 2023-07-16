ROOT = "root"

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

    def set_number(self, n):
        self.n = n

    def set_operation(self, a, b, operation):
        self.a = a
        self.b = b
        self.operation = operation

    # Call out number.
    def call(self):
        if self.n is not None:
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

        # Create monkeys:
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


monkeys = load_input("input.txt")

print(monkeys[ROOT].call())
