import sys

# Map values:
ELF = "#"
GROUND = " "
PROPOSED = "P"
UNAVAILABLE = "X"

NORTH = "N"
SOUTH = "S"
WEST = "W"
EAST = "E"
DIRECTIONS = [NORTH, SOUTH, WEST, EAST]

X, Y = 0, 1

TARGET_TILE_INDEX = 1
ADJACENT_TILES = {
    NORTH: [[-1, 1], [0, 1], [1, 1]],
    SOUTH: [[-1, -1], [0, -1], [1, -1]],
    WEST: [[-1, -1], [-1, 0], [-1, 1]],
    EAST: [[1, -1], [1, 0], [1, 1]]
}


# 2D matrix which allows negative coordinates.
class Map:
    def __init__(self):
        self.ne = []
        self.se = []
        self.sw = []
        self.nw = []

        self.min_x = self.min_y = sys.maxsize
        self.max_x = self.max_y = -sys.maxsize - 1

    # Internal method to get the appropriate quadrant.
    def get_quadrant(self, x, y):
        if x >= 0 and y >= 0:
            return self.ne
        elif x >= 0:
            return self.se
        elif y >= 0:
            return self.nw
        else:
            return self.sw

    # Set tile value.
    def set_value(self, x, y, value):
        self.min_x = min(x, self.min_x)
        self.min_y = min(y, self.min_y)
        self.max_x = max(x, self.max_x)
        self.max_y = max(y, self.max_y)

        quadrant = self.get_quadrant(x, y)
        x, y = abs(x), abs(y)

        while y >= len(quadrant):
            quadrant.append([])

        while x >= len(quadrant[y]):
            quadrant[y].append(GROUND)

        quadrant[y][x] = value

    # Get tile value:
    def get_value(self, x, y):
        quadrant = self.get_quadrant(x, y)
        x, y = abs(x), abs(y)

        if y < len(quadrant) and x < len(quadrant[y]):
            return quadrant[y][x]

        return GROUND

    # Clear all non-elf tiles.
    def clear_proposed(self):
        for quadrant in [self.ne, self.se, self.sw, self.nw]:
            for y in range(len(quadrant)):
                for x in range(len(quadrant[y])):
                    if quadrant[y][x] != ELF:
                        quadrant[y][x] = GROUND

    # Count ground tiles in the smallest possible rectangle.
    def get_ground_count(self):
        # Find smallest rectangle that contains all elfs:
        min_x = min_y = sys.maxsize
        max_x = max_y = -sys.maxsize - 1
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                if self.get_value(x, y) == ELF:
                    min_x = min(x, min_x)
                    min_y = min(y, min_y)
                    max_x = max(x, max_x)
                    max_y = max(y, max_y)

        # Count ground tiles:
        ground_count = 0
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.get_value(x, y) == GROUND:
                    ground_count += 1

        return ground_count


# Character that can move along a map.
class Elf:
    def __init__(self, x, y, map):
        self.x = x
        self.y = y

        self.map = map
        self.map.set_value(x, y, ELF)

        self.proposed_x = self.proposed_y = None

    # Return true if all surrounding tiles are empty, otherwise false.
    def is_clear(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx != 0 or dy != 0) and self.map.get_value(self.x + dx, self.y + dy) == ELF:
                    return False

        return True

    # Analyze surrounding tiles and propose move.
    def consider_move(self, directions):
        if self.is_clear():
            return

        for direction in directions:
            should_propose_move = True

            for adjacent_tile in ADJACENT_TILES[direction]:
                if self.map.get_value(self.x + adjacent_tile[X], self.y + adjacent_tile[Y]) == ELF:
                    should_propose_move = False
                    break

            if should_propose_move:
                adjacent_tile = ADJACENT_TILES[direction][TARGET_TILE_INDEX]
                self.proposed_x = self.x + adjacent_tile[X]
                self.proposed_y = self.y + adjacent_tile[Y]

                # If proposed tile is available, mark as proposed, otherwise mark as unavailable:
                if map.get_value(self.proposed_x, self.proposed_y) == GROUND:
                    map.set_value(self.proposed_x, self.proposed_y, PROPOSED)
                else:
                    map.set_value(self.proposed_x, self.proposed_y, UNAVAILABLE)
                break

    # Move to proposed tile, if available.
    # Return true if a move is made, otherwise false.
    def move(self):
        if self.proposed_x is None or self.proposed_y is None:
            return False

        has_moved = False

        if map.get_value(self.proposed_x, self.proposed_y) == PROPOSED:
            map.set_value(self.x, self.y, GROUND)
            map.set_value(self.proposed_x, self.proposed_y, ELF)

            self.x, self.y = self.proposed_x, self.proposed_y
            has_moved = True

        self.proposed_x = self.proposed_y = None

        return has_moved


def load_input(path):
    input = []

    with open(path) as file:
        for line in file:
            input.insert(0, line.strip())

    return input


# Load and parse input:
input = load_input("input.txt")
map = Map()
elves = []
directions = DIRECTIONS

# Create elves and populate map:
for y in range(len(input)):
    for x in range(len(input[y])):
        if input[y][x] == ELF:
            elves.append(Elf(x, y, map))

# Run until no elves move:
round_count = 0
while True:
    has_moved = False

    for elf in elves:
        elf.consider_move(directions)

    for elf in elves:
        if elf.move():
            has_moved = True

    map.clear_proposed()
    directions.append(directions.pop(0))

    round_count += 1

    if not has_moved:
        break

print(round_count)
