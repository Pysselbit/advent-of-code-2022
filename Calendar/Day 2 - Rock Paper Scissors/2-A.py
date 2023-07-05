A_ROCK = "X"
A_PAPER = "Y"
A_SCISSORS = "Z"

B_ROCK = "A"
B_PAPER = "B"
B_SCISSORS = "C"

WIN_SCORE = 6
DRAW_SCORE = 3

ROCK_SCORE = 1
PAPER_SCORE = 2
SCISSORS_SCORE = 3


def get_score(a, b):
    score = 0

    if a == A_ROCK:
        score += ROCK_SCORE

        if b == B_ROCK:
            score += DRAW_SCORE
        elif b == B_SCISSORS:
            score += WIN_SCORE

    if a == A_PAPER:
        score += PAPER_SCORE

        if b == B_PAPER:
            score += DRAW_SCORE
        elif b == B_ROCK:
            score += WIN_SCORE

    if a == A_SCISSORS:
        score += SCISSORS_SCORE

        if b == B_SCISSORS:
            score += DRAW_SCORE
        elif b == B_PAPER:
            score += WIN_SCORE

    return score


total_score = 0

with open("input.txt") as file:
    for line in file:
        round = line.strip().split(" ")
        total_score += get_score(round[1], round[0])

print(total_score)
