import ast
import functools


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


# Load input into packet list.
def load_input(path):
    packets = []

    with open(path) as file:
        lines = file.readlines();

        for i in range(0, len(lines), 3):
            packets.append(ast.literal_eval(lines[i].strip()))
            packets.append(ast.literal_eval(lines[i + 1].strip()))

    return packets


divider_packet_a = [[2]]
divider_packet_b = [[6]]

# Load input and add divider packets:
packets = load_input("input.txt")
packets.append(divider_packet_a)
packets.append(divider_packet_b)

packets.sort(key = functools.cmp_to_key(compare))

# Locate divider packets:
divider_packet_a_index = divider_packet_b_index = -1
for i in range(0, len(packets)):
    if packets[i] == divider_packet_a:
        divider_packet_a_index = i + 1
    if packets[i] == divider_packet_b:
        divider_packet_b_index = i + 1

print(divider_packet_a_index * divider_packet_b_index)
