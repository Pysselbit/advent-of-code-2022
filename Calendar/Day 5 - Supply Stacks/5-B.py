import re

MOVE = 0
FROM = 1
TO = 2


def parse_crates(path):
    file = open(path)
    lines = file.readlines()
    lines.reverse()
    file.close()

    stack_count = (len(lines[0]) + 1) // 4

    stacks = []
    while len(stacks) < stack_count:
        stacks.append([])

    for line in lines:
        for i in range(0, stack_count):
            index = 4 * i + 1 # Index of IDs in the format "[A] [B] [C]..."

            if index <= len(line) and line[index].isalpha():
                stacks[i].append(line[index])

    return stacks


def parse_moves(path):
    moves = []

    with open(path) as file:
        for line in file:
            # Extract numbers from line:
            move = re.findall(r'\d+', line)
            move = list(map(int, move))

            # Change from 1 indexed to 0 indexed:
            move[FROM] -= 1
            move[TO] -= 1

            moves.append(move)

    return moves


crates = parse_crates("input_crates.txt")
moves = parse_moves("input_moves.txt")

# Move crates:
for move in moves:
    temp = []
    while move[MOVE] > 0:
        temp.append(crates[move[FROM]].pop())
        move[MOVE] -= 1

    while len(temp) > 0:
        crates[move[TO]].append(temp.pop())

# Find top crate IDs:
top_crates = ""
for stack in crates:
    top_crates += stack[-1]

print(top_crates)
