INT_MAX = 9223372036854775807

POS = "pos"
STEPS = "steps"


# 2D vector, containing x and y.
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


map = []
width = height = 0
target_pos = None
step_map = []
move_queue = []


# Return height at pos.
def get_height(pos):
    return map[pos.y][pos.x]


# Return steps needed (as of yet) to get to pos.
def get_steps(pos):
    return step_map[pos.y][pos.x]


# Set steps needed to get to pos.
def set_steps(pos, steps):
    step_map[pos.y][pos.x] = steps


# Return True if pos is within bounds and to_pos is at most 1 higher than from_pos.
def can_move(from_pos, to_pos):
    if to_pos.x < 0 or to_pos.x >= width:
        return False
    if to_pos.y < 0 or to_pos.y >= height:
        return False
    return get_height(to_pos) - get_height(from_pos) <= 1


# Add pos to queue, to be visited and evaluated.
def queue_visit(pos, steps):
    move_queue.append({
        POS: pos,
        STEPS: steps
    })


# Visit and evaluate pos.
def visit(pos, steps):
    if steps >= get_steps(pos):
        return

    set_steps(pos, steps)

    north = Pos(pos.x, pos.y + 1)
    east = Pos(pos.x + 1, pos.y)
    south = Pos(pos.x, pos.y - 1)
    west = Pos(pos.x - 1, pos.y)

    if can_move(pos, north):
        queue_visit(north, steps + 1)
    if can_move(pos, east):
        queue_visit(east, steps + 1)
    if can_move(pos, south):
        queue_visit(south, steps + 1)
    if can_move(pos, west):
        queue_visit(west, steps + 1)


# Return a list of all positions at elevation 0.
def find_low_points():
    low_points = []

    for x in range(0, width):
        for y in range(0, height):
            pos = Pos(x, y)

            if get_height(pos) == 0:
                low_points.append(pos)

    return low_points


def reset_step_map():
    for x in range(0, width):
        for y in range(0, height):
            set_steps(Pos(x, y), INT_MAX)


# Load input:
with open("input.txt") as file:
    lines = file.readlines()

    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for y in range(0, len(lines)):
        row = []
        step_row = []

        for x in range(0, len(lines[y])):
            letter = lines[y][x]

            if letter == "S":
                height = alphabet.find("a")
            elif letter == "E":
                target_pos = Pos(x, y)
                height = alphabet.find("z")
            else:
                height = alphabet.find(letter)

            row.append(height)
            step_row.append(INT_MAX)

        map.append(row)
        step_map.append(step_row)

    width = len(map[0])
    height = len(map)

shortest_path = INT_MAX

# For each pos with elevation 0, evaluate all paths and find the shortest path to target:
low_points = find_low_points()
for starting_pos in low_points:
    reset_step_map()

    visit(starting_pos, 0)
    while len(move_queue) > 0:
        move = move_queue.pop(0)
        visit(move[POS], move[STEPS])

    if get_steps(target_pos) < shortest_path:
        shortest_path = get_steps(target_pos)

print(shortest_path)
