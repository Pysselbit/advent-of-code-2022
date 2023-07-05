
with open("input.txt") as file:
    stream = file.read().strip()

for i in range(14, len(stream)):
    is_start_of_packet = True

    for j in range(1, 14):
        for k in range(j + 1, 15):
            if stream[i - j] == stream[i - k]:
                is_start_of_packet = False

    if is_start_of_packet:
        print(i)
        break