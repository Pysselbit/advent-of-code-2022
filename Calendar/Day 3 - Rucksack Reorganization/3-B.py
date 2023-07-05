LOWER_CASE_ITEMS = "abcdefghijklmnopqrstuvwxyz"
UPPER_CASE_ITEMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_priority(item):
    if item.islower():
        return 1 + LOWER_CASE_ITEMS.find(item)
    else:
        return 27 + UPPER_CASE_ITEMS.find(item)


def get_badge(group):
    for item in group[0]:
        if (group[1].find(item) >= 0 and group[2].find(item) >= 0):
            return item


total_priority = 0

with open("input.txt") as file:
    group = []

    for line in file:
        group.append(line.strip())

        if len(group) == 3:
            total_priority += get_priority(get_badge(group))
            group = []

print(total_priority)
