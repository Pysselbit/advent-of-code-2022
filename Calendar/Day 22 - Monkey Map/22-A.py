OFF_MAP = " "
EMPTY = "."
WALL = "#"

RIGHT, LEFT = "R", "L"
EAST, SOUTH, WEST, NORTH = "E", "S", "W", "N"
DIRECTIONS = [EAST, SOUTH, WEST, NORTH]


# A navigator that can traverse a map.
class Navigator:
    def __init__(self, map, x, y, direction):
        self.map = map,
        self.map_width = len(map[0])
        self.map_height = len(map)

        self.x = x
        self.y = y
        self.direction = direction

    # Move in the current direction.
    def move(self, steps):
        if self.direction == EAST:
            dx = 1
        elif self.direction == WEST:
            dx = -1
        else:
            dx = 0

        if self.direction == SOUTH:
            dy = 1
        elif self.direction == NORTH:
            dy = -1
        else:
            dy = 0

        while steps > 0:
            next_x = (self.x + dx) % self.map_width
            next_y = (self.y + dy) % self.map_height

            while map[next_y][next_x] != EMPTY:
                # Stop when next position is a wall:
                if map[next_y][next_x] == WALL:
                    next_x, next_y = self.x, self.y
                    steps = 0
                    break

                # Wrap around the edge:
                next_x = (next_x + dx) % self.map_width
                next_y = (next_y + dy) % self.map_height

            self.x, self.y = next_x, next_y
            steps -= 1

    # Turn left or right.
    def turn(self, direction):
        if direction == RIGHT:
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) + 1) % len(DIRECTIONS)]
        else:
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) - 1) % len(DIRECTIONS)]


def load_input(path):
    with open(path) as file:
        lines = [line.rstrip() for line in file.readlines()]

        map_input = lines[0:len(lines) - 2]
        path_input = lines[-1]

        return map_input, path_input


def parse_map_input(map_input):
    width = 0

    for line in map_input:
        width = max(len(line), width)

    map = []

    for line in map_input:
        map.append(line + OFF_MAP * (width - len(line)))

    return map


def parse_path_input(path_input):
    path = []
    i = 0
    while i < len(path_input):
        step = path_input[i]

        if step.isalpha():
            path.append(step)

        elif step.isdigit():
            while i + 1 < len(path_input) and path_input[i + 1].isdigit():
                step += path_input[i + 1]
                i += 1
            path.append(int(step))

        i += 1

    return path


# Get input data:
map_input, path_input = load_input("input.txt")
map = parse_map_input(map_input)
path = parse_path_input(path_input)

navigator = Navigator(map, map[0].find(EMPTY), 0, EAST)

# Follow path on map:
for step in path:
    if isinstance(step, int):
        navigator.move(step)
    else:
        navigator.turn(step)

print(1000 * (navigator.y + 1) + 4 * (navigator.x + 1) + DIRECTIONS.index(navigator.direction))
