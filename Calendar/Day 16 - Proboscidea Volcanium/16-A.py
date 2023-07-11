import re

VALVE = "valve"
FLOW_RATE = "flow_rate"
EDGES = "edges"

INPUT_VALVE = 1
INPUT_FLOW_RATE = 4
INPUT_EDGES = 9

START_NODE = "AA"
START_TIME = 30


# Graph node with edges and some metadata.
class Node:
    def __init__(self, valve, flow_rate):
        self.valve = valve
        self.flow_rate = flow_rate
        self.edges = []


# Graph edge with a target and a cost (time to traverse).
class Edge:
    def __init__(self, target, cost):
        self.target = target
        self.cost = cost


# Get raw input as a list.
def load_input(path):
    input = []

    with open(path) as file:
        for line in file:
            words = line.strip().split(" ")

            valve = words[INPUT_VALVE]
            flow_rate = int(re.findall(r'\d+', words[INPUT_FLOW_RATE])[0])

            edges = []
            for i in range(INPUT_EDGES, len(words)):
                edges.append(re.sub(r'[^a-zA-Z]', '', words[i]))

            input.append({
                VALVE: valve,
                FLOW_RATE: flow_rate,
                EDGES: edges
            })

    return input


# Create graph with nodes and edges.
def create_graph(input):
    graph = {}

    for item in input:
        graph[item[VALVE]] = Node(item[VALVE], item[FLOW_RATE])

    for item in input:
        node = graph[item[VALVE]]

        for link in item[EDGES]:
            node.edges.append(Edge(graph[link], 1))

    return graph


# Create complete graph with all zero value nodes (except start node) removed.
def trim_graph(graph, start_node):
    included_nodes = [start_node]

    # Exclude zero value nodes:
    for key in graph:
        if graph[key].flow_rate > 0:
            included_nodes.append(graph[key])

    # Calculate distances from each node to each other node:
    distances = []
    for a in included_nodes:
        distances.append([])

        for b in included_nodes:
            distances[-1].append(get_distance(a, b))

    # Create graph that only includes non-zero nodes (and the start node):
    trimmed_graph = {}
    for node in included_nodes:
        trimmed_graph[node.valve] = Node(node.valve, node.flow_rate)

    # Add edges with pre-calculated costs:
    for i in range(0, len(included_nodes)):
        node = trimmed_graph[included_nodes[i].valve]

        for j in range(0, len(included_nodes)):
            if i == j:
                continue

            node.edges.append(Edge(trimmed_graph[included_nodes[j].valve], distances[i][j]))

    return trimmed_graph


# Get total cost to traverse between two nodes (using BFS).
def get_distance(a, b):
    visited = []
    queue = [[a, 0]]

    while len(queue) > 0:
        item = queue.pop(0)
        a = item[0]
        cost = item[1]

        if a == b:
            return cost

        for edge in a.edges:
            if edge.target not in visited:
                queue.append([edge.target, cost + edge.cost])

        visited.append(a)


# Get max pressure release possible within the given time.
def get_max_pressure_release(node, time, total_pressure_release=0, visited=""):
    if time <= 0:
        return total_pressure_release

    if node.valve != START_NODE:  # First one is not turned.
        time -= 1

    total_pressure_release += time * node.flow_rate
    visited += node.valve

    # Try all possible routes:
    max_pressure_release = total_pressure_release
    for edge in node.edges:
        should_visit = True

        for i in range(0, len(visited), 2):
            if visited[i:i + 2] == edge.target.valve:
                should_visit = False
                break

        if should_visit:
            pressure_release = get_max_pressure_release(edge.target, time - edge.cost, total_pressure_release, visited)

            if pressure_release > max_pressure_release:
                max_pressure_release = pressure_release

    return max_pressure_release


graph = create_graph(load_input("input.txt"))
trimmed_graph = trim_graph(graph, graph[START_NODE])
start_node = trimmed_graph[START_NODE]

print(get_max_pressure_release(start_node, START_TIME))
