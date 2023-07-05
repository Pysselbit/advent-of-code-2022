grid = []

# Load input:
with open("input.txt") as file:
    for line in file:
        grid.append(line.strip())

W = len(grid)
H = len(grid[0])

visible_count = 0

# Count visible trees:
for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        tree = grid[y][x]
        if y == 0 or x == 0 or y == H - 1 or x == W - 1:
            visible_count += 1
            continue

        tree = grid[y][x]
        vis_up = vis_left = vis_down = vis_right = True

        # Check up, left, down and right for blocking trees:
        for dy in range(1, y + 1):
            if grid[y - dy][x] >= tree:
                vis_up = False
        for dx in range(1, x + 1):
            if grid[y][x - dx] >= tree:
                vis_left = False
        for dy in range(1, H - y):
            if grid[y + dy][x] >= tree:
                vis_down = False
        for dx in range(1, W - x):
            if grid[y][x + dx] >= tree:
                vis_right = False

        if vis_up or vis_left or vis_down or vis_right:
            visible_count +=1

print(visible_count)