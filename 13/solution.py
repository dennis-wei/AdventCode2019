import sys
from collections import defaultdict
import time
import math
from copy import deepcopy

from computer import Computer

mapping = {
    0: ' ',
    1: '|',
    2: 'x',
    3: '_',
    4: 'o'
}

def get_input():
    raw_input = sys.stdin.read()
    return raw_input

def get_input_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()
    
def parse_input(input):
    return [int(n) for n in input.strip().split(',')]

def get_num_blocks(grid):
    return sum(v == 'x' for v in grid.values())

def get_ball_paddle(grid):
    # is_o = False
    for k, v in grid.items():
        if v == 'o':
            ball_coord = k
        if v == '_':
            paddle_coord = k

    return ball_coord, paddle_coord

def init_step(computer, grid):
    num_loops = 0
    score = 0
    while(True):
        (bx, by), (px, py) = get_ball_paddle(grid)
        if bx < px:
            i = -1
        elif bx == px:
            i = 0
        elif bx > px:
            i = 1
        output = computer.run_on_input([i])
        split = [output[i:i+3] for i in range(0, len(output), 3)]
        for x, y, t in split:
            if x == -1 and y == 0:
                new_score = t
            else:
                grid[(x, y)] = mapping[t]

        num_blocks = get_num_blocks(grid)
        if num_blocks == 0:
            return new_score

        # if num_loops % 500 == 0:
        #     print(num_blocks)
        #     print_grid(grid)
        #     print()
        num_loops += 1
    
def print_grid(grid):
    minx = min(t[0] for t in grid.keys())
    maxx = max(t[0] for t in grid.keys())
    miny = min(t[1] for t in grid.keys())
    maxy = max(t[1] for t in grid.keys())

    for i in range(miny, maxy):
        for j in range(minx, maxx):
            print(grid[(j, i)], end='')
        print()

def main():
    start = time.time()
    # Part 1
    i = parse_input(get_input_from_file('input.txt'))
    computer = Computer(i)
    output = computer.run_on_input([])
    split = [output[i:i+3] for i in range(0, len(output), 3)]
    a1 = len(list(filter(lambda x: x[2] == 2, split)))
    print("Answer to Part 1: ", a1)
    print(f"Took {time.time() - start} seconds")

    # Part 2
    grid = defaultdict(lambda: ' ')
    for x, y, t in split:
        grid[(x, y)] = mapping[t]
    
    # print_grid(grid)

    a2 = init_step(computer, grid)
    print("Answer to Part 2: ", a2)
    print(f"Took {time.time() - start} seconds")
main()