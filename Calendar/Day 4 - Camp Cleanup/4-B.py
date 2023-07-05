def overlaps(a, b):
    if a[1] >= b[0] and a[0] <= b[1]:
        return True
    if b[1] >= a[0] and b[0] <= a[1]:
        return True
    return False


def parse_range(range):
    range = range.split("-")
    return [int(range[0]), int(range[1])]


contained_count = 0

with open("input.txt") as file:
    for line in file:
        ranges = line.strip().split(",")

        a = parse_range(ranges[0])
        b = parse_range(ranges[1])

        if overlaps(a, b):
            contained_count += 1

print(contained_count)
