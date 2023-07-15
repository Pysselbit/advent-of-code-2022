INDEX = 0
VALUE = 1

KEY = 811589153

# Get input as list of tuples (line index, line value * decryption key):
items = []
with open("input.txt") as file:
    lines = file.readlines()

    for j in range(len(lines)):
        items.append((j, int(lines[j].strip()) * KEY))

n = len(items)

# Mix 10 times:
for i in range(10):
    # Move all items its value's number of steps:
    for j in range(n):
        # Find the current item's current list index:
        for k in range(n):
            if items[k][INDEX] == j:
                break

        # Get number of steps to move item (modulo n - 1 since a loop has n - 1 steps):
        steps = items[k][VALUE]
        steps = steps % (n - 1) if steps > 0 else steps % -(n - 1)

        # When steps > 0, move item forward:
        while steps > 0:
            # If at end of list, move to beginning:
            if k + 1 == n:
                items.insert(0, items.pop())
                k = 0

            # Switch places with next item:
            items[k + 1], items[k] = items[k], items[k + 1]

            # Update item list index and reduce number of steps to move:
            k += 1
            steps -= 1

        # When steps < 0, move item backward:
        while steps < 0:
            # If at beginning of list, move to end:
            if k - 1 < 0:
                items.append(items.pop(0))
                k = n - 1

            # Switch places with previous item:
            items[k - 1], items[k] = items[k], items[k - 1]

            # Update item list index and reduce number of steps to move:
            k -= 1
            steps += 1

            # If item ends up at the beginning of the list, it should move to the end (according to the example):
            if k - 1 < 0:
                items.append(items.pop(0))
                k = n - 1

# Find index of item with value 0:
for j in range(n):
    if items[j][VALUE] == 0:
        zero_index = j

# Get x, y, and z coordinates:
x = items[(zero_index + 1000) % n][VALUE]
y = items[(zero_index + 2000) % n][VALUE]
z = items[(zero_index + 3000) % n][VALUE]

print(x + y + z)
