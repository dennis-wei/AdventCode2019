import networkx as nx
from collections import defaultdict
import time
from copy import deepcopy
import matplotlib.pyplot as plt

def build_grid(filename):
    with open(filename, 'r') as f:
        lines = f.read().split("\n")

    grid = defaultdict(lambda: "#")
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c in set(["."]) or c.isupper():
                grid[(x, y)] = c
    
    center = (len(lines[0]) // 2, len(lines) // 2)

    return grid, center


def get_adjacent(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

def get_inner_outer(c1, c2, center):
    dist_c1 = abs(center[0] - c1[0]) + abs(center[1] - c1[1])
    dist_c2 = abs(center[0] - c2[0]) + abs(center[1] - c2[1])
    if dist_c1 < dist_c2:
        return c1, c2
    elif dist_c1 == dist_c2:
        # print(f"Equal: {c1} | {c2}")
        return c1, c2
    else:
        return c2, c1


def build_graph(grid, center, is_part_2 = False):
    NUM_LEVELS = 45
    G = nx.Graph()
    nodes = set(grid.keys())
    portals = defaultdict(set)
    for k, v in deepcopy(grid).items():
        if v == ".":
            for adj in get_adjacent(*k):
                if adj in grid and grid[adj] == ".":
                    for l in range(NUM_LEVELS):
                        x1, y1 = k
                        x2, y2 = adj
                        G.add_edge((x1, y1, l), (x2, y2, l), weight = 1)

        elif v.isupper():
            is_portal = False
            portal_coord = None
            other_letter = None
            other_coord = None
            exit_coord = None
            for adj in get_adjacent(*k):
                if grid[adj] == ".":
                    is_portal = True
                    exit_coord = adj
                elif grid[adj].isupper():
                    other_letter = grid[adj]
                    other_coord = adj
            if not other_letter:
                raise "Expected another letter"
            ordered = "".join(sorted(f"{v}{other_letter}"))
            if is_portal:
                portals[ordered].add(k)
                portal_coord = k
            else:
                portals[ordered].add(other_coord)
                portal_coord = other_coord
                for adj in get_adjacent(*other_coord):
                    if grid[adj] == ".":
                        exit_coord = adj
            
            assert portal_coord
            assert exit_coord
            x1, y1 = portal_coord
            x2, y2 = exit_coord
            if v == "A" or v == "Z":
                G.add_edge((x1, y1, 0), (x2, y2, 0), weight = 0)
            else:
                for l in range(NUM_LEVELS):
                    G.add_edge((x1, y1, l), (x2, y2, l), weight = 0)
    
    assert "AA" in portals
    assert "ZZ" in portals
    for portal, coords in portals.items():
        if portal in set(["AA", "ZZ"]):
            assert len(coords) == 1
        assert len(coords) <= 2
        if len(coords) == 2:
            c1, c2 = list(coords)
            if not is_part_2:
                x1, y1 = c1
                x2, y2 = c2
                G.add_edge((x1, y1, 0), (x2, y2, 0), weight = 1)
            else:
                inner, outer = get_inner_outer(c1, c2, center)
                # print(f"Portal {portal} | inner: {inner} | outer: {outer}")
                for l in range(NUM_LEVELS - 1):
                    x1, y1 = inner
                    x2, y2 = outer
                    G.add_edge((x1, y1, l), (x2, y2, l + 1), weight = 1)
    
    return G, portals

def part1(filename):
    grid, center = build_grid(filename)
    G, portals = build_graph(grid, center)
    sx, sy = list(portals["AA"])[0]
    ex, ey = list(portals["ZZ"])[0]

    start = (sx, sy, 0)
    end = (ex, ey, 0)

    try:
        path = nx.shortest_path(G, start, end, weight="weight")
        # for i in range(len(nx.shortest_path(G, start, end, weight="weight")) - 1):
        #     n1 = path[i]
        #     n2 = path[i + 1]
        #     print(f"{n1} -> {n2}: {G.get_edge_data(n1, n2)}")

        a1 = nx.shortest_path_length(G, start, end, weight="weight")
        print("Answer to Part 1: ", a1)
    except:
        print("No path exists")

def part2(filename):
    grid, center = build_grid(filename)
    G, portals = build_graph(grid, center, True)
    # print(portals)
    inv_portals = {}
    for k, l in portals.items():
        for c in l:
            inv_portals[c] = k
    sx, sy = list(portals["AA"])[0]
    ex, ey = list(portals["ZZ"])[0]

    start = (sx, sy, 0)
    end = (ex, ey, 0)

    try:
        # test = nx.shortest_path(G, start, (21, 27, 10), weight="weight")
        # print(test)

        a2 = nx.shortest_path_length(G, start, end, weight="weight")
        print("Answer to Part 2: ", a2)
    except:
        print("No path exists")

start = time.time()
filename = "input.txt"
part1(filename)
print(f"Took {time.time() - start} seconds for Part 1")
part2(filename)
print(f"Took {time.time() - start} seconds for both parts")