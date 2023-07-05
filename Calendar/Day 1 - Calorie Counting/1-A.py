max = 0

with open("input.txt") as file:
    total = 0

    for line in file:
        line = line.strip()

        if line.isdigit():
            total += int(line)
        else:
            if total > max:
                max = total

            total = 0

print(max)
