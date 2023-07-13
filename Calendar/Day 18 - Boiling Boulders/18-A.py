import sys

X = 0
Y = 1
Z = 2

# Load input:
positions = []
with open("input.txt") as file:
    for line in file:
        coordinates = [int(i) for i in line.strip().split(",")]
        positions.append([coordinates[X], coordinates[Y], coordinates[Z]])

# Get min and max positions:
min_x = min_y = min_z = sys.maxsize
max_x = max_y = max_z = -sys.maxsize - 1
for position in positions:
    min_x, min_y, min_z = min(position[X], min_x), min(position[Y], min_y), min(position[Z], min_z)
    max_x, max_y, max_z = max(position[X], max_x), max(position[Y], max_y), max(position[Z], max_z)

# Calculate matrix size:
size_x = max_x - min_x + 1
size_y = max_y - min_y + 1
size_z = max_z - min_z + 1

# Shift positions to fit in matrix:
dx = -min_x
dy = -min_y
dz = -min_z

# Create empty matrix:
matrix = []
for x in range(0, size_x):
    matrix.append([])
    for y in range(0, size_y):
        matrix[-1].append([])
        for z in range(0, size_z):
            matrix[-1][-1].append(False)

# Fill matrix with input positions:
for position in positions:
    matrix[position[X] + dx][position[Y] + dy][position[Z] + dz] = True

# Count exposed surfaces:
area = 0
for x in range(0, size_x):
    for y in range(0, size_y):
        for z in range(0, size_z):
            if matrix[x][y][z]:
                if x - 1 < 0 or not matrix[x - 1][y][z]:
                    area += 1
                if x + 1 == size_x or not matrix[x + 1][y][z]:
                    area += 1
                if y - 1 < 0 or not matrix[x][y - 1][z]:
                    area += 1
                if y + 1 == size_y or not matrix[x][y + 1][z]:
                    area += 1
                if z - 1 < 0 or not matrix[x][y][z - 1]:
                    area += 1
                if z + 1 == size_z or not matrix[x][y][z + 1]:
                    area += 1

print(area)