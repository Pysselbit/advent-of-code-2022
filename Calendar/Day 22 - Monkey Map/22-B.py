OFF_MAP = " "
EMPTY = "."
WALL = "#"

# Directions:
RIGHT, LEFT = "R", "L"
EAST, SOUTH, WEST, NORTH = "E", "S", "W", "N"
DIRECTIONS = [EAST, SOUTH, WEST, NORTH]
NW, NE, SE, SW = "NW", "NE", "SE", "SW"

# Cube edge data indices:
FROM_FACE = 0
FROM_DIRECTION = 1
FROM_A = 2
FROM_B = 3
TO_FACE = 4
TO_DIRECTION = 5
TO_A = 6
TO_B = 7
TARGET_POSITION = 0
TARGET_DIRECTION = 1

MAP_LAYOUT = [
    " 12",
    " 3 ",
    "45 ",
    "6  "
]

MAP_EDGES = [
    (1, WEST, SW, NW, 4, EAST, NW, SW),
    (1, NORTH, NW, NE, 6, EAST, NW, SW),
    (2, NORTH, NW, NE, 6, NORTH, SW, SE),
    (2, EAST, NE, SE, 5, WEST, SE, NE),
    (2, SOUTH, SE, SW, 3, WEST, SE, NE),
    (3, EAST, NE, SE, 2, NORTH, SW, SE),
    (5, EAST, NE, SE, 2, WEST, SE, NE),
    (5, SOUTH, SE, SW, 6, WEST, SE, NE),
    (6, EAST, NE, SE, 5, NORTH, SW, SE),
    (6, SOUTH, SE, SW, 2, SOUTH, NE, NW),
    (6, WEST, SW, NW, 1, SOUTH, NE, NW),
    (4, WEST, SW, NW, 1, EAST, NW, SW),
    (4, NORTH, NW, NE, 3, EAST, NW, SW),
    (3, WEST, SW, NW, 4, SOUTH, NE, NW)
]


# 2D vector, containing x and y.
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


# A navigator that can traverse a cube map.
class Navigator:
    def __init__(self, map, edge_map, x, y, direction):
        self.map = map,
        self.edge_map = edge_map
        self.map_width = len(map[0])
        self.map_height = len(map)

        self.x = x
        self.y = y
        self.direction = direction

    # Move in the current direction.
    def move(self, steps):
        while steps > 0:
            edges = self.edge_map[self.y][self.x]

            # See if passing a cube edge:
            if edges and self.direction in edges:
                edge = edges[self.direction]
                next_x = edge[TARGET_POSITION].x
                next_y = edge[TARGET_POSITION].y
                next_direction = edge[TARGET_DIRECTION]

            # If not, just keep moving straight.
            else:
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

                next_x = self.x + dx
                next_y = self.y + dy
                next_direction = self.direction

            # Stop when next position is a wall:
            if map[next_y][next_x] == WALL:
                next_x, next_y = self.x, self.y
                next_direction = self.direction
                steps = 0
                break

            self.x, self.y = next_x, next_y
            self.direction = next_direction
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
    map_layout = []
    edge_map = []

    for line in map_input:
        map.append(line + OFF_MAP * (width - len(line)))
        edge_map.append([None for i in range(width)])

    # Scale up map layout to match map size:
    scale = len(map_input) // len(MAP_LAYOUT)
    for line in MAP_LAYOUT:
        scaled_line = ""
        for c in line:
            scaled_line += scale * c
        for i in range(scale):
            map_layout.append(scaled_line)

    # Find corners (NW, NE, SE, and SW) for each cube face:
    nws, nes, ses, sws = {}, {}, {}, {}
    for y in range(len(map_layout)):
        for x in range(len(map_layout[y])):
            if map_layout[y][x].isdigit() and int(map_layout[y][x]) not in nws:
                nws[int(map_layout[y][x])] = Pos(x, y)
        for x in range(len(map_layout[y]) - 1, -1, -1):
            if map_layout[y][x].isdigit() and int(map_layout[y][x]) not in nes:
                nes[int(map_layout[y][x])] = Pos(x, y)
    for y in range(len(map_layout) - 1, -1, -1):
        for x in range(len(map_layout[y])):
            if map_layout[y][x].isdigit() and int(map_layout[y][x]) not in sws:
                sws[int(map_layout[y][x])] = Pos(x, y)
        for x in range(len(map_layout[y]) - 1, -1, -1):
            if map_layout[y][x].isdigit() and int(map_layout[y][x]) not in ses:
                ses[int(map_layout[y][x])] = Pos(x, y)

    # Create faces with four corners each, along with their corner positions:
    faces = {}
    for i in range(1, 7):
        faces[i] = {
            NW: nws[i],
            NE: nes[i],
            SW: sws[i],
            SE: ses[i]
        }

    # Map positions of all edges onto edge map:
    for edge in MAP_EDGES:
        from_a = faces[edge[FROM_FACE]][edge[FROM_A]]
        from_b = faces[edge[FROM_FACE]][edge[FROM_B]]
        from_direction = edge[FROM_DIRECTION]

        to_a = faces[edge[TO_FACE]][edge[TO_A]]
        to_b = faces[edge[TO_FACE]][edge[TO_B]]
        to_direction = edge[TO_DIRECTION]

        # Get delta positions of source and target edge:
        from_dx = from_dy = to_dx = to_dy = 0
        if from_a.x != from_b.x:
            from_dx = 1 if from_b.x > from_a.x else -1
        elif from_a.y != from_b.y:
            from_dy = 1 if from_b.y > from_a.y else -1
        if to_a.x != to_b.x:
            to_dx = 1 if to_b.x > to_a.x else -1
        elif to_a.y != to_b.y:
            to_dy = 1 if to_b.y > to_a.y else -1

        # Iterate from a to b (of source and target edge) and populate edge map:
        from_x, from_y = from_a.x, from_a.y
        to_x, to_y = to_a.x, to_a.y
        while True:
            if edge_map[from_y][from_x] is None:
                edge_map[from_y][from_x] = {}
            edge_map[from_y][from_x][from_direction] = (Pos(to_x, to_y), to_direction)

            if from_x == from_b.x and from_y == from_b.y:
                break

            from_x += from_dx
            from_y += from_dy
            to_x += to_dx
            to_y += to_dy

    return map, edge_map


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
map, edge_map = parse_map_input(map_input)
path = parse_path_input(path_input)

navigator = Navigator(map, edge_map, map[0].find(EMPTY), 0, EAST)

# Follow path on map:
for step in path:
    if isinstance(step, int):
        navigator.move(step)
    else:
        navigator.turn(step)

print(1000 * (navigator.y + 1) + 4 * (navigator.x + 1) + DIRECTIONS.index(navigator.direction))
