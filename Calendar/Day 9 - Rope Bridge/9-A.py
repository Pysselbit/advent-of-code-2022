DIRECTION = 0
STEPS = 1

X, Y = 0, 1
UP, DOWN, LEFT, RIGHT = "U", "D", "L", "R"

h_pos, t_pos = [0, 0], [0, 0]

marks = []


def move_head(direction):
    if direction == UP:
        h_pos[Y] += 1
    elif direction == DOWN:
        h_pos[Y] -= 1
    elif direction == LEFT:
        h_pos[X] -= 1
    elif direction == RIGHT:
        h_pos[X] += 1


def move_tail():
    if abs(h_pos[X] - t_pos[X]) <= 1 and abs(h_pos[Y] - t_pos[Y]) <= 1:
        return

    if h_pos[X] - t_pos[X] > 1:
        t_pos[X] = h_pos[X] - 1
        t_pos[Y] = h_pos[Y]
    elif h_pos[Y] - t_pos[Y] > 1:
        t_pos[Y] = h_pos[Y] - 1
        t_pos[X] = h_pos[X]
    elif t_pos[X] - h_pos[X] > 1:
        t_pos[X] = h_pos[X] + 1
        t_pos[Y] = h_pos[Y]
    elif t_pos[Y] - h_pos[Y] > 1:
        t_pos[Y] = h_pos[Y] + 1
        t_pos[X] = h_pos[X]


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
        mark_pos(t_pos)
        move[STEPS] -= 1

print(len(marks))