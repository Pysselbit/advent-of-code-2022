import re

MIN = 0
MAX = 4000000

SENSOR = 0
BEACON = 1
DISTANCE = 2

INPUT_SENSOR_X = 0
INPUT_SENSOR_Y = 1
INPUT_BEACON_X = 2
INPUT_BEACON_Y = 3


# 2D vector, containing x and y.
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


def get_distance(a, b):
    return abs(b.x - a.x) + abs(b.y - a.y)


# Load sensor and beacon positions and calculate their relative distances.
def load_input(path):
    input = []

    with open(path) as file:
        for line in file:
            coordinates = list(map(int, re.findall(r'[-]?\d+', line.strip())))

            sensor = Pos(coordinates[INPUT_SENSOR_X], coordinates[INPUT_SENSOR_Y])
            beacon = Pos(coordinates[INPUT_BEACON_X], coordinates[INPUT_BEACON_Y])

            distance = get_distance(sensor, beacon)

            input.append([sensor, beacon, distance])

    return input


input = load_input("input.txt")

beacon_pos = None

# Find the one available position:
for y in range(MIN, MAX + 1):
    if beacon_pos is not None:
        break

    x = MIN

    while x <= MAX:
        pos = Pos(x, y)

        is_available = True
        next_x = 0

        # Check if position is within range of any sensor:
        for item in input:
            if get_distance(pos, item[SENSOR]) <= item[DISTANCE]:
                is_available = False

                # Find the right border of this sensor's area (to skip unnecessary coordinates):
                right_border_x = item[SENSOR].x + item[DISTANCE] - abs(item[SENSOR].y - y) + 1
                if right_border_x > next_x:
                    next_x = right_border_x

        if is_available:
            beacon_pos = pos
            break

        x = next_x

print(beacon_pos.x * 4000000 + beacon_pos.y)
