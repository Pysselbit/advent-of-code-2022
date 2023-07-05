DIRECTION = 0
STEPS = 1

X, Y = 0, 1
UP, DOWN, LEFT, RIGHT = "U", "D", "L", "R"

HEAD = 0
TAIL = 9

rope = []
while len(rope) <= TAIL:
    rope.append([0, 0])

marks = []


def move_head(direction):
    if direction == UP:
        rope[HEAD][Y] += 1
    elif direction == DOWN:
        rope[HEAD][Y] -= 1
    elif direction == LEFT:
        rope[HEAD][X] -= 1
    elif direction == RIGHT:
        rope[HEAD][X] += 1


def move_tail():
    for i in range(1, len(rope)):
        a = rope[i - 1]
        b = rope[i]

        if abs(a[X] - b[X]) <= 1 and abs(a[Y] - b[Y]) <= 1:
            continue

        if a[X] - b[X] > 1:
            b[X] = a[X] - 1
            if a[Y] - b[Y] > 1:
                b[Y] = a[Y] - 1
            elif b[Y] - a[Y] > 1:
                b[Y] = a[Y] + 1
            else:
                b[Y] = a[Y]
        elif a[Y] - b[Y] > 1:
            b[Y] = a[Y] - 1
            if a[X] - b[X] > 1:
                b[X] = a[X] - 1
            elif b[X] - a[X] > 1:
                b[X] = a[X] + 1
            else:
                b[X] = a[X]
        elif b[X] - a[X] > 1:
            b[X] = a[X] + 1
            if a[Y] - b[Y] > 1:
                b[Y] = a[Y] - 1
            elif b[Y] - a[Y] > 1:
                b[Y] = a[Y] + 1
            else:
                b[Y] = a[Y]
        elif b[Y] - a[Y] > 1:
            b[Y] = a[Y] + 1
            if a[X] - b[X] > 1:
                b[X] = a[X] - 1
            elif b[X] - a[X] > 1:
                b[X] = a[X] + 1
            else:
                b[X] = a[X]


def mark_pos(pos):
    # Lazy. Should've been done with a grid, but ... negative indices: fugde it.
    for mark in marks:
        if pos[X] == mark[X] and pos[Y] == mark[Y]:
            return

    marks.append([pos[X], pos[Y]])


moves = []

# Load input:
with open("input.txt") as file:
    for line in file:
        move = line.strip().split(" ")
        moves.append([move[0], int(move[1])])

# Perform moves:
for move in moves:
    while move[STEPS] > 0:
        move_head(move[DIRECTION])
        move_tail()
        mark_pos(rope[TAIL])
        move[STEPS] -= 1

print(len(marks))