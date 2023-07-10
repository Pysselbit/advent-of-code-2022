import sys
import re

TARGET_Y = 2000000

SENSOR = "sensor"
BEACON = "beacon"

MARK_UNMARKED = 0
MARK_SENSOR = 1
MARK_BEACON = 2
MARK_NO_BEACON = 3

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


# List that can have negative coordinates.
class Row:
    def __init__(self, y, min_pos, max_pos, padding):
        self.y = y
        self.dx = -min_pos.x + padding

        width = max_pos.x - min_pos.x + 1 + 2 * padding

        self.row = []
        for x in range(0, width):
            self.row.append(MARK_UNMARKED)

    def get_value(self, x):
        return self.row[x + self.dx]

    def set_value(self, x, value):
        self.row[x + self.dx] = value


def load_input(path):
    input = []

    with open(path) as file:
        for line in file:
            coordinates = list(map(int, re.findall(r'[-]?\d+', line.strip())))
            input.append({
                SENSOR: Pos(coordinates[INPUT_SENSOR_X], coordinates[INPUT_SENSOR_Y]),
                BEACON: Pos(coordinates[INPUT_BEACON_X], coordinates[INPUT_BEACON_Y])
            })

    return input


# Create row and add input sensors and beacons (if their y coordinates match).
def create_row(input):
    min_pos = Pos(sys.maxsize, sys.maxsize)
    max_pos = Pos(-sys.maxsize - 1, -sys.maxsize - 1)
    max_distance = 0

    for item in input:
        min_pos.x = min(item[SENSOR].x, item[BEACON].x, min_pos.x)
        min_pos.y = min(item[SENSOR].y, item[BEACON].y, min_pos.y)
        max_pos.x = max(item[SENSOR].x, item[BEACON].x, max_pos.x)
        max_pos.y = max(item[SENSOR].y, item[BEACON].y, max_pos.y)
        max_distance = max(abs(item[BEACON].x - item[SENSOR].x) + abs(item[BEACON].y - item[SENSOR].y), max_distance)

    row = Row(TARGET_Y, min_pos, max_pos, max_distance)

    for item in input:
        if item[SENSOR].y == row.y:
            row.set_value(item[SENSOR].x, MARK_SENSOR)
        if item[BEACON].y == row.y:
            row.set_value(item[BEACON].x, MARK_BEACON)

    return row


# Calculate and mark unavailable beacon positions.
def mark_unavailable_positions(row, input):
    for item in input:
        sensor = item[SENSOR]
        beacon = item[BEACON]

        distance = abs(beacon.x - sensor.x) + abs(beacon.y - sensor.y)
        dy = abs(TARGET_Y - sensor.y)

        for dx in range(0, distance - dy + 1):
            if row.get_value(sensor.x + dx) == MARK_UNMARKED:
                row.set_value(sensor.x + dx, MARK_NO_BEACON)
            if row.get_value(sensor.x - dx) == MARK_UNMARKED:
                row.set_value(sensor.x - dx, MARK_NO_BEACON)


input = load_input("input.txt")
target_row = create_row(input)
mark_unavailable_positions(target_row, input)

# Count unavailable beacon positions:
no_beacon_count = 0
for value in target_row.row:
    if value == MARK_NO_BEACON:
        no_beacon_count += 1

print(no_beacon_count)
