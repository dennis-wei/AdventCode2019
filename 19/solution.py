from computer import Computer
import time
from collections import defaultdict
import math
import sys

def print_grid(grid):
    minx = min(t[0] for t in grid.keys())
    maxx = max(t[0] for t in grid.keys())
    miny = min(t[1] for t in grid.keys())
    maxy = max(t[1] for t in grid.keys())

    for i in range(miny, maxy + 1):
        for j in range(minx, maxx + 1):
            print(grid[(j, i)], end='')
        print()
    print()

def write_grid(grid):
    minx = min(t[0] for t in grid.keys())
    maxx = max(t[0] for t in grid.keys())
    miny = min(t[1] for t in grid.keys())
    maxy = max(t[1] for t in grid.keys())

    with open("cache.txt", 'w+') as f:
        for i in range(miny, maxy + 1):
            for j in range(minx, maxx + 1):
                f.write(f"{grid[(j, i)]}")
            f.write("\n")

def get_can_fit(one_coords, square_side, x, y):
    # print(x, y)
    if (x + square_side - 1, y) in one_coords and (x, y + square_side - 1) in one_coords:
        return True
    
    return False

def parse_cache(split_lines):
    cache = defaultdict(int)
    one_coords = set()
    for y, l in enumerate(split_lines):
        for x, c in enumerate(l):
            output = int(c)
            coord = (int(x), int(y))
            cache[coord] = output
            if output == 1:
                one_coords.add((x, y))
    
    if len(one_coords) > 0:
        maxx = max(c[0] for c in one_coords)
        maxx_filtered = [c for c in one_coords if c[0] == maxx]
        miny = min(c[1] for c in maxx_filtered)
        top_right = (maxx, miny)

        maxy = max(c[1] for c in one_coords)
        maxy_filtered = [c for c in one_coords if c[1] == maxy]
        minx = min(c[0] for c in maxy_filtered)
        bottom_left = (minx, maxy)
    else:
        bottom_left = (0, 0)
        top_right = (0, 0)
    
    print("bottom_left: ", bottom_left)
    print("top_right: ", top_right)
    return cache, one_coords, bottom_left, top_right

def main(filename):
    start = time.time()
    with open(filename, 'r') as f:
        code = [int(n) for n in f.read().strip().split(",")]
    
    with open("cache.txt", 'r+') as f:
        grid, one_coords, bottom_left, top_right = parse_cache([l.strip() for l in f])
    
    for y in range(1050):
        for x in range(1050):
            if (x, y) not in grid:
                if x < bottom_left[0] and y > bottom_left[1]:
                    # print(f"Skipping {(x, y)} because of bottom right")
                    continue
                if x > top_right[0] and y < top_right[1]:
                    # print(f"Skipping {(x, y)} because of top right")
                    continue

                computer = Computer(code[:])
                output = computer.run_on_input([x, y])[0]
                if output == 1:
                    one_coords.add((x, y))
                    if y > bottom_left[1] and x >= bottom_left[0]:
                        # print("Setting bottom left to: ", (x, y))
                        bottom_left = (x, y)
                    if x > top_right[0] and y >= top_right[1]:
                        # print("Setting top right to: ", (x, y))
                        top_right = (x, y)
                grid[(x, y)] = output

    write_grid(grid)
    
    # print_grid(grid)
    print("Solution to Part 1: ", len(one_coords))
    print(f"Took {time.time() - start} seconds for Part 1")

    can_fit_dict = {}
    sorted_coords = sorted(one_coords, key = lambda c: c[0] + c[1])
    for c in sorted_coords:
        can_fit = get_can_fit(one_coords, 100, *c)
        if can_fit:
            a2 = 10000 * c[0] + c[1]
            print("Solution to Part 2: ", a2)
            print(f"Took {time.time() - start} seconds for both parts")
            return
    # print_grid(grid)
    # print(can_fit_dict)

main("input.txt")