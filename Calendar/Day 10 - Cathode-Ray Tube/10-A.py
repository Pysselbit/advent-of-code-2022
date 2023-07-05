ADDX = "addx"
NOOP = "noop"

MEASURE_CYCLES = [20, 60, 100, 140, 180, 220]

x = 1
cycle = 1

signal_strength_sum = 0

with open("input.txt") as file:
    for line in file:
        instruction = line.strip().split(" ")

        if cycle in MEASURE_CYCLES:
            signal_strength_sum += cycle * x

        if instruction[0] == NOOP:
            cycle += 1

        if instruction[0] == ADDX:
            cycle += 1
            if cycle in MEASURE_CYCLES:
                signal_strength_sum += cycle * x

            x += int(instruction[1])
            cycle += 1

print(signal_strength_sum)
