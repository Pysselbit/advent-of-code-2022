SNAFU_TO_DECIMAL = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

DECIMAL_TO_SNAFU = {v: k for k, v in SNAFU_TO_DECIMAL.items()}


def snafu_to_decimal(s):
    n = 0
    exp = 0

    for c in s[::-1]:
        n += pow(5, exp) * SNAFU_TO_DECIMAL[c]
        exp += 1

    return n


def decimal_to_snafu(n):
    s = ""

    while n != 0:
        d = (n + 2) % 5 - 2
        s = DECIMAL_TO_SNAFU[d] + s
        n = (n - d) // 5

    return s


def load_input(path):
    with open(path) as file:
        return [line.strip() for line in file.readlines()]


snafus = load_input("input.txt")

print(decimal_to_snafu(sum([snafu_to_decimal(snafu) for snafu in snafus])))
