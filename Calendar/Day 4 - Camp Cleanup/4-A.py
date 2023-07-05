def contains(outer, inner):
    return inner[0] >= outer[0] and inner[1] <= outer[1]


def parse_range(range):
    range = range.split("-")
    return [int(range[0]), int(range[1])]


contained_count = 0

with open("input.txt") as file:
    for line in file:
        ranges = line.strip().split(",")

        a = parse_range(ranges[0])
        b = parse_range(ranges[1])

        if contains(a, b) or contains(b, a):
            contained_count += 1

print(contained_count)
