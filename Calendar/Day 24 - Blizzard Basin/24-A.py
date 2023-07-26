CLEAR = "."
WALL = "#"

NORTH = "^"
EAST = ">"
SOUTH = "v"
WEST = "<"

BLIZZARD_ORDER = [NORTH, EAST, SOUTH, WEST]

X = 0
Y = 1
TIME = 2

VICINITY = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]


# Entity that can move and populate a map.
class Blizzard:
    def __init__(self, x, y, direction, map):
        self.x = x
        self.y = y

        self.dx = 1 if direction == EAST else -1 if direction == WEST else 0
        self.dy = 1 if direction == NORTH else -1 if direction == SOUTH else 0

        self.map = map

    # Move one step on map.
    def move(self):
        self.map[self.y][self.x] -= 1

        self.x += self.dx
        self.y += self.dy

        # Wrap around edge:
        while map[self.y][self.x] == WALL:
            self.x = (self.x + self.dx) % len(map[self.y])
            self.y = (self.y + self.dy) % len(map)

        self.map[self.y][self.x] += 1


# Load input as map and blizzards.
def load_input(path):
    map = []
    blizzards = []

    with open(path) as file:
        lines = [line.strip() for line in reversed(file.readlines())]

        for y in range(len(lines)):
            map.append([])

            for x in range(len(lines[y])):
                value = lines[y][x]

                if value == WALL:
                    map[-1].append(WALL)
                elif value in BLIZZARD_ORDER:
                    blizzards.append(Blizzard(x, y, value, map))
                    map[-1].append(1)
                else:
                    map[-1].append(0)

    return map, blizzards


map, blizzards = load_input("input.txt")

# Find start and goal tiles:
start_y, goal_y = len(map) - 1, 0
start_x, goal_x = map[start_y].index(0), map[goal_y].index(0)

# Map to prevent duplicate states in queue:
time_map = [[[] for x in range(len(map[y]))] for y in range(len(map))]

# Create queue and add starting position:
total_time = -1
queue = [(start_x, start_y, total_time + 1)]

# Run BFS until goal is reached or queue is empty:
has_reached_goal = False
while not has_reached_goal and len(queue) > 0:
    visit = queue.pop(0)

    # See if goal has been reached:
    if visit[X] == goal_x and visit[Y] == goal_y:
        has_reached_goal = True
        break

    # Move blizzards if all queue items of previous timestamp has been handled:
    if visit[TIME] > total_time:
        for blizzard in blizzards:
            blizzard.move()
        total_time += 1

    # Look for possible moves in the vicinity:
    for tile in VICINITY:
        x = visit[X] + tile[X]
        y = visit[Y] + tile[Y]
        time = visit[TIME] + 1

        if y == len(map):
            continue

        if map[y][x] == 0:
            while len(time_map[y][x]) < time + 1:
                time_map[y][x].append(False)

            # Only add to queue if state (position and timestamp) is unique:
            if not time_map[y][x][time]:
                queue.append((x, y, time))
                time_map[y][x][time] = True

print(total_time)
