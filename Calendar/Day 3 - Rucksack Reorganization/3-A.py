LOWER_CASE_ITEMS = "abcdefghijklmnopqrstuvwxyz"
UPPER_CASE_ITEMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_priority(item):
    if item.islower():
        return 1 + LOWER_CASE_ITEMS.find(item)
    else:
        return 27 + UPPER_CASE_ITEMS.find(item)


total_priority = 0

with open("input.txt") as file:
    for line in file:
        line = line.strip()

        a = line[0:len(line) // 2]
        b = line[len(line) // 2:len(line)]

        shared_item = ""

        for item in a:
            if b.find(item) >= 0:
                shared_item = item
                break

        total_priority += get_priority(shared_item)

print(total_priority)
