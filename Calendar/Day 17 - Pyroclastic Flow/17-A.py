AIR = "."
ROCK = "#"
FLOOR = "-"

LEFT = "<"
RIGHT = ">"
DOWN = "v"

CAVE_SHAFT_WIDTH = 7

N_ROCKS = 2022


# Cave with a cave shaft and possibility to add falling rocks to build a tower.
class Cave:
    def __init__(self, width):
        self.shaft = [[FLOOR] * width]

        self.width = width
        self.height = 1

        self.falling_rock = None
        self.falling_rock_x = self.falling_rock_y = 0

    def __str__(self):
        s = ""

        for y in range(self.height - 1, 0, -1):
            s += "|"
            for x in self.shaft[y]:
                s += x
            s += "|\n"

        return s + "+" + (FLOOR * self.width) + "+"

    def get_tower_height(self):
        for y in range(self.height - 1, 0, -1):
            if ROCK in self.shaft[y]:
                return y

        return 0

    def add_level(self):
        self.shaft.append([AIR] * self.width)
        self.height += 1

    def add_falling_rock(self, rock):
        self.falling_rock = rock
        self.falling_rock_x = 2
        self.falling_rock_y = self.get_tower_height() + 4

    def affix_falling_rock(self):
        for y in range(0, len(self.falling_rock)):
            while self.falling_rock_y + y + 1 >= self.height:
                self.add_level()

            for x in range(0, len(self.falling_rock[y])):
                if self.falling_rock[y][x] == ROCK:
                    self.shaft[self.falling_rock_y + y][self.falling_rock_x + x] = ROCK

        self.falling_rock = None

    def can_move_falling_rock(self, direction):
        dx = dy = 0

        if direction == LEFT:
            dx = -1
        elif direction == RIGHT:
            dx = 1
        elif direction == DOWN:
            dy = -1

        for y in range(0, len(self.falling_rock)):
            for x in range(0, len(self.falling_rock[y])):
                if self.falling_rock[y][x] == AIR:
                    continue

                new_x = self.falling_rock_x + x + dx
                new_y = self.falling_rock_y + y + dy

                if new_x < 0 or new_x >= self.width or new_y <= 0:
                    return False

                if new_y >= self.height:
                    continue

                if self.shaft[new_y][new_x] == ROCK:
                    return False

        return True

    def apply_jet(self, direction):
        if self.can_move_falling_rock(direction):
            if direction == LEFT:
                self.falling_rock_x -= 1
            elif direction == RIGHT:
                self.falling_rock_x += 1

    def apply_gravity(self):
        if self.can_move_falling_rock(DOWN):
            self.falling_rock_y -= 1
        else:
            self.affix_falling_rock()

    def has_falling_rock(self):
        return self.falling_rock is not None


def load_rocks(path):
    rocks = []
    rock = []

    with open(path) as file:
        for line in file:
            line = line.strip()

            if line == "":
                rocks.append(rock)
                rock = []
            else:
                rock_segment = []

                for c in line:
                    rock_segment.append(ROCK if c == ROCK else AIR)

                rock.insert(0, rock_segment)

    rocks.append(rock)

    return rocks


def load_input(path):
    list = []

    with open(path) as file:
        input = file.read().strip()
        for c in input:
            list.append(c)

    return list


# Load input:
jets = load_input("input.txt")
rocks = load_rocks("rocks.txt")
cave = Cave(CAVE_SHAFT_WIDTH)

jet_index = 0

# Add n falling rocks to build tower:
for i in range(0, N_ROCKS):
    cave.add_falling_rock(rocks[i % len(rocks)])

    # Apply jets and gravity until affixed:
    while cave.has_falling_rock():
        cave.apply_jet(jets[jet_index])
        cave.apply_gravity()

        jet_index = (jet_index + 1) % len(jets)

print(cave.get_tower_height())
