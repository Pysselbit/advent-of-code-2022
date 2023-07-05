MAX_SIZE = 100000

CMD_PREFIX = "$"
CMD_CD = "cd"
CMD_LS = "ls"

CD_ROOT = "/"
CD_UP = ".."

LS_DIR = "dir"

DIRS = "directories"
FILES = "files"
NAME = "name"
PARENT = "parent"
SIZE = "size"


def new_directory(name, parent):
    return {
        NAME: name,
        PARENT: parent,
        DIRS: {},
        FILES: {},
        SIZE: None
    }


# Recursively calculate size of a directory and its children.
def calculate_size(dir):
    size = 0

    for d in dir[DIRS]:
        calculate_size(dir[DIRS][d])
        size += dir[DIRS][d][SIZE]

    for f in dir[FILES]:
        size += dir[FILES][f]

    dir[SIZE] = size


# Recurse through a directory and its children.
# Return the sum of all directory sizes not exceeding the max limit.
def sum_dirs(dir, max_size):
    total_size = 0

    if dir[SIZE] <= max_size:
        total_size += dir[SIZE]

    for d in dir[DIRS]:
        total_size += sum_dirs(dir[DIRS][d], max_size)

    return total_size


root_dir = new_directory("root", None)
current_dir = None

with open("input.txt") as file:
    for line in file:
        cmd = line.strip().split(" ")

        if cmd[0] == CMD_PREFIX and cmd[1] == CMD_CD:
            if cmd[2] == CD_ROOT:
                current_dir = root_dir
            elif cmd[2] == CD_UP:
                current_dir = current_dir[PARENT]
            else:
                current_dir = current_dir[DIRS][cmd[2]]
            continue

        if cmd[0] == CMD_PREFIX and cmd[1] == CMD_LS:
            continue

        if cmd[0] == LS_DIR:
            name = cmd[1]
            if name not in current_dir[DIRS].keys():
                current_dir[DIRS][name] = new_directory(name, current_dir)
            continue

        if cmd[0].isdigit():
            name = cmd[1]
            if name not in current_dir[FILES].keys():
                current_dir[FILES][name] = int(cmd[0])
            continue

calculate_size(root_dir)

print(sum_dirs(root_dir, MAX_SIZE))
