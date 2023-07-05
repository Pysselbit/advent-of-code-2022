ADDX = "addx"
NOOP = "noop"

ON = "#"
OFF = "."

WIDTH = 40

x = 1

display = [""]


def draw_pixel():
    pixel = ON if x - 1 <= len(display[-1]) <= x + 1 else OFF

    display[-1] = display[-1] + pixel

    if len(display[-1]) == 40:
        display.append("")


with open("input.txt") as file:
    for line in file:
        instruction = line.strip().split(" ")

        draw_pixel()

        if instruction[0] == ADDX:
            draw_pixel()
            x += int(instruction[1])

for line in display:
    print(line)
