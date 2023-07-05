grid = []

# Load input:
with open("input.txt") as file:
    for line in file:
        grid.append(line.strip())

W = len(grid)
H = len(grid[0])

best_score = 0

# Score each tree, looking for the highest score:
for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        tree = grid[y][x]
        if y == 0 or x == 0 or y == H - 1 or x == W - 1:
            continue

        tree = grid[y][x]
        score_up = score_left = score_down = score_right = 0

        # Look up, left, down and right, counting visible trees:
        for dy in range(1, y + 1):
            score_up += 1
            if grid[y - dy][x] >= tree:
                break
        for dx in range(1, x + 1):
            score_left += 1
            if grid[y][x - dx] >= tree:
                break
        for dy in range(1, H - y):
            score_down += 1
            if grid[y + dy][x] >= tree:
                break
        for dx in range(1, W - x):
            score_right += 1
            if grid[y][x + dx] >= tree:
                break

        score = score_up * score_left * score_down * score_right
        if score > best_score:
            best_score = score

print(best_score)