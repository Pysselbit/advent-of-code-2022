import re

TIME = 32

BLUEPRINT_ID = 0
ORE_ROBOT_ORE_COST = 1
CLAY_ROBOT_ORE_COST = 2
OBSIDIAN_ROBOT_ORE_COST = 3
OBSIDIAN_ROBOT_CLAY_COST = 4
GEODE_ROBOT_ORE_COST = 5
GEODE_ROBOT_OBSIDIAN_COST = 6


def load_input(path):
    blueprints = []

    with open(path) as file:
        for line in file:
            values = [int(i) for i in re.findall(r'\d+', line)]

            blueprints.append([
                values[BLUEPRINT_ID],
                values[ORE_ROBOT_ORE_COST],
                values[CLAY_ROBOT_ORE_COST],
                values[OBSIDIAN_ROBOT_ORE_COST],
                values[OBSIDIAN_ROBOT_CLAY_COST],
                values[GEODE_ROBOT_ORE_COST],
                values[GEODE_ROBOT_OBSIDIAN_COST]
            ])

    return blueprints


# Get max geode count possible for the given blueprint and time.
def get_max_geode_count(blueprint, time,
                        ore_robot_count=1, clay_robot_count=0, obsidian_robot_count=0, geode_robot_count=0,
                        ore_count=0, clay_count=0, obsidian_count=0, geode_count=0,
                        may_build_ore_robot=True, may_build_clay_robot=True, may_build_obsidian_robot=True, may_build_geode_robot=True):
    if time == 0:
        return geode_count

    # Do not build robots for resources that are already at capacity:
    should_build_ore_robot = ore_robot_count < max(blueprint[ORE_ROBOT_ORE_COST],
                                                   blueprint[CLAY_ROBOT_ORE_COST],
                                                   blueprint[OBSIDIAN_ROBOT_ORE_COST],
                                                   blueprint[GEODE_ROBOT_ORE_COST])
    should_build_clay_robot = clay_robot_count < blueprint[OBSIDIAN_ROBOT_CLAY_COST]
    should_build_obsidian_robot = obsidian_robot_count < blueprint[GEODE_ROBOT_OBSIDIAN_COST]

    # Check which robots we can afford:
    can_build_ore_robot = ore_count >= blueprint[ORE_ROBOT_ORE_COST]
    can_build_clay_robot = ore_count >= blueprint[CLAY_ROBOT_ORE_COST]
    can_build_obsidian_robot = ore_count >= blueprint[OBSIDIAN_ROBOT_ORE_COST] \
                               and clay_count >= blueprint[OBSIDIAN_ROBOT_CLAY_COST]
    can_build_geode_robot = ore_count >= blueprint[GEODE_ROBOT_ORE_COST] \
                            and obsidian_count >= blueprint[GEODE_ROBOT_OBSIDIAN_COST]

    # Geode robots should be built as soon as possible:
    if can_build_geode_robot:
        should_build_ore_robot = should_build_clay_robot = should_build_obsidian_robot = False

    # Extract resources for each robot:
    ore_count += ore_robot_count
    clay_count += clay_robot_count
    obsidian_count += obsidian_robot_count
    geode_count += geode_robot_count

    max_geode_count = 0

    # Try building an ore robot:
    if may_build_ore_robot and should_build_ore_robot and can_build_ore_robot:
        max_geode_count = max(get_max_geode_count(blueprint, time - 1,
                                                  ore_robot_count + 1,
                                                  clay_robot_count,
                                                  obsidian_robot_count,
                                                  geode_robot_count,
                                                  ore_count - blueprint[ORE_ROBOT_ORE_COST],
                                                  clay_count,
                                                  obsidian_count,
                                                  geode_count),
                              max_geode_count)

    # Try building a clay robot:
    if may_build_clay_robot and should_build_clay_robot and can_build_clay_robot:
        max_geode_count = max(get_max_geode_count(blueprint, time - 1,
                                                  ore_robot_count,
                                                  clay_robot_count + 1,
                                                  obsidian_robot_count,
                                                  geode_robot_count,
                                                  ore_count - blueprint[CLAY_ROBOT_ORE_COST],
                                                  clay_count,
                                                  obsidian_count,
                                                  geode_count),
                              max_geode_count)

    # Try building an obsidian robot:
    if may_build_obsidian_robot and should_build_obsidian_robot and can_build_obsidian_robot:
        max_geode_count = max(get_max_geode_count(blueprint, time - 1,
                                                  ore_robot_count,
                                                  clay_robot_count,
                                                  obsidian_robot_count + 1,
                                                  geode_robot_count,
                                                  ore_count - blueprint[OBSIDIAN_ROBOT_ORE_COST],
                                                  clay_count - blueprint[OBSIDIAN_ROBOT_CLAY_COST],
                                                  obsidian_count,
                                                  geode_count),
                              max_geode_count)

    # Try building a geode robot:
    if may_build_geode_robot and can_build_geode_robot:
        max_geode_count = max(get_max_geode_count(blueprint, time - 1,
                                                  ore_robot_count,
                                                  clay_robot_count,
                                                  obsidian_robot_count,
                                                  geode_robot_count + 1,
                                                  ore_count - blueprint[GEODE_ROBOT_ORE_COST],
                                                  clay_count,
                                                  obsidian_count - blueprint[GEODE_ROBOT_OBSIDIAN_COST],
                                                  geode_count),
                              max_geode_count)

    # Instead of building robots, wait one minute, to gather resources:
    # For the next round only allow building robots that could not be afforded this round.
    max_geode_count = max(get_max_geode_count(blueprint, time - 1,
                                              ore_robot_count,
                                              clay_robot_count,
                                              obsidian_robot_count,
                                              geode_robot_count,
                                              ore_count,
                                              clay_count,
                                              obsidian_count,
                                              geode_count,
                                              not can_build_ore_robot,
                                              not can_build_clay_robot,
                                              not can_build_obsidian_robot,
                                              not can_build_geode_robot),
                          max_geode_count)

    return max_geode_count


blueprints = load_input("input.txt")

# Find the max geode counts of the first three blueprints and multiply them together:
geode_count_product = 1
for i in range(3):
    geode_count_product *= get_max_geode_count(blueprints[i], TIME)

print(geode_count_product)