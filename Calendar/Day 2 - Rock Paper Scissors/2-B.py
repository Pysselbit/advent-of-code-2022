ROCK = "A"
PAPER = "B"
SCISSORS = "C"

LOSS = "X"
DRAW = "Y"
WIN = "Z"


def get_score(a, b):
    score = 0

    if a == ROCK:
        score += 1

        if b == ROCK:
            score += 3
        elif b == SCISSORS:
            score += 6

    if a == PAPER:
        score += 2

        if b == PAPER:
            score += 3
        elif b == ROCK:
            score += 6

    if a == SCISSORS:
        score += 3

        if b == SCISSORS:
            score += 3
        elif b == PAPER:
            score += 6

    return score


def get_shape(opponent, result):
    if result == WIN:
        if opponent == ROCK:
            return PAPER
        if opponent == PAPER:
            return SCISSORS
        else:
            return ROCK

    if result == LOSS:
        if opponent == ROCK:
            return SCISSORS
        if opponent == PAPER:
            return ROCK
        else:
            return PAPER

    return opponent


total_score = 0

with open("input.txt") as file:
    for line in file:
        round = line.strip().split(" ")
        total_score += get_score(get_shape(round[0], round[1]), round[0])

print(total_score)
