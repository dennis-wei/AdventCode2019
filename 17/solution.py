from computer import Computer
import time
from collections import defaultdict
import math

def parse_input(filename):
    with open(filename, 'r') as f:
        return [int(n) for n in f.read().strip().split(',')]

def get_adjacent(x, y):
    return [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

def print_grid(grid):
    minx = min(t[0] for t in grid.keys())
    maxx = max(t[0] for t in grid.keys())
    miny = min(t[1] for t in grid.keys())
    maxy = max(t[1] for t in grid.keys())

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[(x, y)], end='')
        print()
    print()

def part1():
    code = parse_input("input.txt")
    computer = Computer(code)
    output = computer.run_on_input([])
    as_ascii = [chr(n) for n in output]
    rows = "".join(as_ascii).split("\n")

    grid = defaultdict(lambda: ".")
    scaffolding = set()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            grid[(x, y)] = c
            if c == '#':
                scaffolding.add((x, y))
            # print(c, end="")
        # print()
    
    intersections = set()
    a1 = 0
    for c in scaffolding:
        if all(a in scaffolding for a in get_adjacent(*c)):
            intersections.add(c)
            grid[c] = "0"
            a1 += c[0] * c[1]
    
    print_grid(grid)
    print("Answer to Part 1: ", a1)

def part2():
    ascii_answer = "A,B,B,A,C,B,C,C,B,A\n" + \
        "R,10,R,8,L,10,L,10\n" + \
        "R,8,L,6,L,6\n" + \
        "L,10,R,10,L,6\n" + \
        "n\n"
    

    raw_answer = [ord(c) for c in ascii_answer] 
    print(raw_answer)

    code = parse_input("input.txt")
    code[0] = 2

    computer = Computer(code)
    output = computer.run_on_input(raw_answer)
    as_ascii = [chr(n) for n in output[:-1]]
    rows = "".join(as_ascii).split("\n")

    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            print(c, end="")
        print()

    print("Answer to Part 2: ", output[-1])

start = time.time()
part1()
print(f"Took {time.time() - start} seconds for Part 1")
part2()
print(f"Took {time.time() - start} seconds for both parts")