max = [0, 0, 0]

with open("input.txt") as file:
    total = 0

    for line in file:
        line = line.strip()

        if line.isdigit():
            total += int(line)
        else:
            if total > max[0]:
                max[0], max[1], max[2] = total, max[0], max[1]
            elif total > max[1]:
                max[1], max[2] = total, max[1]
            elif total > max[2]:
                max[2] = total

            total = 0

print(max[0] + max[1] + max[2])
