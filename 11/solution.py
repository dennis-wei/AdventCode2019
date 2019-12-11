import time
from collections import defaultdict

from computer import Computer

with open('input.txt', 'r') as f:
    line = f.read().strip()
    problem_input = [int(n) for n in line.split(',')]

# with open('sample_input1.txt', 'r') as f:
#     line = f.read().strip()
#     problem_input = [int(n) for n in line.split(',')]

class RobotGrid:
    def __init__(self, initial_color):
        self.robot_coords = (0, 0)
        self.grid = defaultdict(lambda: '.')
        self.grid[(0, 0)] = initial_color
        self.robot_dir = "N"
        self.painted = set()
    
    def rotate_on_output(self, output):
        left_mapping = {
            "N": "W",
            "W": "S",
            "S": "E",
            "E": "N"
        }

        right_mapping = {
            "N": "E",
            "E": "S",
            "S": "W",
            "W": "N"
        }

        if output == 0:
            self.robot_dir = left_mapping[self.robot_dir]
        elif output == 1:
            self.robot_dir = right_mapping[self.robot_dir]
        else:
            raise f"UNKNOWN ROTATION DIRECTION: {output}"
    
    def move(self):
        mapping = {
            "N": (0, 1),
            "E": (1, 0),
            "S": (0, -1),
            "W": (-1, 0)
        }

        self.robot_coords = tuple(map(sum, zip(self.robot_coords, mapping[self.robot_dir])))
    
    def paint_on_output(self, output):
        if output == 0:
            self.grid[self.robot_coords] = '.'
            self.painted.add(self.robot_coords)
        elif output == 1:
            self.grid[self.robot_coords] = '#'
            self.painted.add(self.robot_coords)
        else:
            raise f"UNKNOWN PAINT COLOR: {output}"
    
    def step(self, output):
        # print(f"Robot got results: {output}")
        color_output, turn_output = output
        self.paint_on_output(color_output)
        self.rotate_on_output(turn_output)
        self.move()
    
    def print_grid(self):
        minx = min(c[0] for c in self.grid.keys()) - 1
        maxx = max(c[0] for c in self.grid.keys()) + 1
        miny = min(c[1] for c in self.grid.keys()) - 1
        maxy = max(c[1] for c in self.grid.keys()) + 1

        for y in range(maxy + 1, miny - 1, -1):
            for x in range(minx - 1, maxx + 1):
                print(self.grid[(x, y)], end='')
            print()

def main():
    start = time.time()
    computer = Computer(problem_input)
    robot_grid = RobotGrid('.')
    while not computer.halted:
        color_below = robot_grid.grid[robot_grid.robot_coords]
        new_input = {'.': 0, '#': 1}[color_below]
        output = computer.run_on_input([new_input])
        # print(f"Main output: {output}")
        robot_grid.step(output)
    
    print(f"Solution to Part 1: {len(robot_grid.painted)} panels")
    print(f"Took {time.time() - start} seconds")
    print()

    start = time.time()
    computer = Computer(problem_input)
    robot_grid = RobotGrid('#')
    while not computer.halted:
        color_below = robot_grid.grid[robot_grid.robot_coords]
        new_input = {'.': 0, '#': 1}[color_below]
        output = computer.run_on_input([new_input])
        # print(f"Main output: {output}")
        robot_grid.step(output)
    robot_grid.print_grid()
    print(f"Took {time.time() - start} seconds")

main()