import sys

GRID = "grid"
DX = "dx"
DY = "dy"

AIR = 0
ROCK = 1
SAND = 2

SAND_SOURCE_X = 500
SAND_SOURCE_Y = 0


# 2D vector, containing x and y.
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


# Load input structures into grid:
def load_grid(path):
    structures = []
    with open(path) as file:
        for line in file:
            structures.append([])
            blocks = line.strip().split(" -> ")

            for block in blocks:
                block = block.split(",")
                structures[-1].append(Pos(int(block[0]), int(block[1])))

    # Find x and y min and max:
    x_min = y_min = sys.maxsize
    x_max = y_max = -sys.maxsize - 1
    for structure in structures:
        for block in structure:
            x_min = min(block.x, x_min)
            y_min = min(block.y, y_min)
            x_max = max(block.x, x_max)
            y_max = max(block.y, y_max)

    # Used to move structures to start at origin (with added empty padding):
    dx = 1 - x_min
    dy = 1
    width = x_max - x_min + 3
    height = y_max + 3

    # Create empty grid:
    grid = []
    for y in range(0, height):
        grid.append([])

        for x in range(0, width):
            grid[-1].append(AIR)

    # Add structures to grid:
    for structure in structures:
        for i in range(0, len(structure) - 1):
            a = structure[i]
            b = structure[i + 1]

            if a.x != b.x:
                for x in range(a.x, b.x, 1 if b.x > a.x else -1):
                    grid[a.y + dy][x + dx] = ROCK
            elif a.y != b.y:
                for y in range(a.y, b.y, 1 if b.y > a.y else -1):
                    grid[y + dy][a.x + dx] = ROCK

            grid[b.y + dy][b.x + dx] = ROCK

    return {
        GRID: grid,
        DX: dx,
        DY: dy
    }


# Drop sand unit from specified position.
# Return true if unit is added, and false if it falls through.
def add_sand_unit(pos, grid):
    def move():
        if grid[pos.y + 1][pos.x] == AIR:
            pos.y = pos.y + 1
            return True
        if grid[pos.y + 1][pos.x - 1] == AIR:
            pos.x, pos.y = pos.x - 1, pos.y + 1
            return True
        if grid[pos.y + 1][pos.x + 1] == AIR:
            pos.x, pos.y = pos.x + 1, pos.y + 1
            return True
        return False

    while move():
        if pos.y + 1 >= len(grid):
            return False

    grid[pos.y][pos.x] = SAND
    return True


input = load_grid("input.txt")

sand_unit_count = 0
while add_sand_unit(Pos(SAND_SOURCE_X + input[DX], SAND_SOURCE_Y + input[DY]), input[GRID]):
    sand_unit_count += 1

print(sand_unit_count)
