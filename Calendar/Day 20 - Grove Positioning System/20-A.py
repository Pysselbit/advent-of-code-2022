INDEX = 0
VALUE = 1

# Get input as list of tuples (line index, line value):
items = []
with open("input.txt") as file:
    lines = file.readlines()

    for i in range(len(lines)):
        items.append((i, int(lines[i].strip())))

n = len(items)

# Move all items its value's number of steps:
for i in range(n):
    # Find the current item's current list index:
    for j in range(n):
        if items[j][INDEX] == i:
            break

    # Get number of steps to move item:
    steps = items[j][VALUE]

    # When steps > 0, move item forward:
    while steps > 0:
        # If at end of list, move to beginning:
        if j + 1 == n:
            items.insert(0, items.pop())
            j = 0

        # Switch places with next item:
        items[j + 1], items[j] = items[j], items[j + 1]

        # Update item list index and reduce number of steps to move:
        j += 1
        steps -= 1

    # When steps < 0, move item backward:
    while steps < 0:
        # If at beginning of list, move to end:
        if j - 1 < 0:
            items.append(items.pop(0))
            j = n - 1

        # Switch places with previous item:
        items[j - 1], items[j] = items[j], items[j - 1]

        # Update item list index and reduce number of steps to move:
        j -= 1
        steps += 1

        # If item ends up at the beginning of the list, it should move to the end (according to the example):
        if j - 1 < 0:
            items.append(items.pop(0))
            j = n - 1

# Find index of item with value 0:
for i in range(n):
    if items[i][VALUE] == 0:
        zero_index = i

# Get x, y, and z coordinates:
x = items[(zero_index + 1000) % n][VALUE]
y = items[(zero_index + 2000) % n][VALUE]
z = items[(zero_index + 3000) % n][VALUE]

print(x + y + z)
