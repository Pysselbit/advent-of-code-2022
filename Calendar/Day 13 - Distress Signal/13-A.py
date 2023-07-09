import ast


# Compare two packets.
# Return negative if left < right, positive if left > right, and otherwise 0.
def compare(left, right):
    if type(left) == type(right) == int:
        return left - right

    if type(left) == list and type(right) == int:
        right = [right]
    if type(left) == int and type(right) == list:
        left = [left]

    if len(left) == len(right) == 0:
        return 0

    for i in range(0, max(len(left), len(right))):
        if i < len(left) and i < len(right):
            comparison = compare(left[i], right[i])
            if comparison < 0:
                return -1
            if comparison > 0:
                return 1
        elif len(left) > len(right):
            return 1
        else:
            return -1

    return 0


# Load input into packet pairs.
def load_input(path):
    pairs = []

    with open(path) as file:
        lines = file.readlines();

        for i in range(0, len(lines), 3):
            pairs.append([
                ast.literal_eval(lines[i].strip()),
                ast.literal_eval(lines[i + 1].strip())
            ])

    return pairs


pairs = load_input("input.txt")

right_order_indices = 0

# Sum indices of correctly ordered pairs:
for i in range(0, len(pairs)):
    if compare(pairs[i][0], pairs[i][1]) <= 0:
        right_order_indices += i + 1

print(right_order_indices)
