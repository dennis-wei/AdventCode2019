import networkx as nx
import time
from collections import defaultdict
from computer import Computer

def get_input(filename):
    with open(filename, 'r') as f:
        return [int(n) for n in f.read().strip().split(',')]

left_mapping = {
    'N': 'W',
    'W': 'S',
    'S': 'E',
    'E': 'N'
}

right_mapping = {
    'N': 'E',
    'W': 'N',
    'S': 'W',
    'E': 'S'
}

dir_mapping = {
    'N': 1,
    'S': 2,
    'W': 3,
    'E': 4
}

dir_coords = {
    'N': (0, 1),
    'S': (0, -1),
    'W': (-1, 0),
    'E': (1, 0)
}

class Grid:
    def __init__(self, computer):
        self.grid = defaultdict(lambda: ' ')
        self.grid[(0, 0)] = 'x'
        self.robot_pos = (0, 0)
        self.robot_dir = 'N'
        self.computer = computer
        self.left_origin = False
    
    def mark_as_wall(self, dir):
        coord_diff = dir_coords[dir]
        wall_coords = tuple(map(sum, zip(coord_diff, self.robot_pos)))
        # print(f"Marking {wall_coords} as wall")
        self.grid[wall_coords] = '#'
    
    def mark_as_floor(self, output):
        # print(f"Marking {self.robot_pos} as floor")
        if output == 1:
            self.grid[self.robot_pos] = '.'
        elif output == 2:
            self.grid[self.robot_pos] = 'o'
    
    def turn_right(self):
        self.robot_dir = right_mapping[self.robot_dir]
    
    def move_in_dir(self, dir, output):
        coord_diff = dir_coords[dir]
        new_coords = tuple(map(sum, zip(coord_diff, self.robot_pos)))
        self.robot_pos = new_coords
        self.mark_as_floor(output)
        self.left_origin = True
    
    def try_left(self):
        # print("Robot is facing ", self.robot_dir)
        # print("Looking left")
        left_dir = left_mapping[self.robot_dir]
        # print("Left is: ", left_dir)
        linput = dir_mapping[left_dir]
        loutput = self.computer.run_on_input([linput])[0]
        # print("Left output: ", loutput)
        if loutput == 0:
            self.mark_as_wall(left_dir)
            # print("Looking forward")
            finput = dir_mapping[self.robot_dir]
            foutput = self.computer.run_on_input([finput])[0]
            # print("Forward output: ", foutput)
            if foutput == 0:
                self.mark_as_wall(self.robot_dir)
                self.turn_right()
            else:
                self.move_in_dir(self.robot_dir, foutput)
        else:
            self.robot_dir = left_dir
            self.move_in_dir(self.robot_dir, loutput)
    
    def print_grid(self):
        grid = self.grid
        # print(grid)
        minx = min(t[0] for t in grid.keys())
        maxx = max(t[0] for t in grid.keys())
        miny = min(t[1] for t in grid.keys())
        maxy = max(t[1] for t in grid.keys())

        arrow_mapping = {
            'N': '^',
            'E': '>',
            'S': 'v',
            'W': '<'
        }

        for i in range(maxy, miny - 1, - 1):
            for j in range(minx, maxx + 1):
                if (j, i) == self.robot_pos:
                    # print(arrow_mapping[self.robot_dir], end='')
                    print(grid[(j, i)], end='')
                else:
                    print(grid[(j, i)], end='')
            print()
        print()
    
    def build_grid(self):
        num_loops = 0
        while self.robot_pos != (0,0) or self.left_origin == False:
            num_loops += 1
            self.try_left()
            # if num_loops % 100 == 0:
            #     self.print_grid()
        
        self.print_grid()
    
    def build_graph(self):
        grid = self.grid
        minx = min(t[0] for t in grid.keys())
        maxx = max(t[0] for t in grid.keys())
        miny = min(t[1] for t in grid.keys())
        maxy = max(t[1] for t in grid.keys())

        G = nx.Graph()

        floors = set(['o', '.', 'x'])
        for k, v in grid.items():
            if v in floors:
                G.add_node(k)
            if v == 'o':
                oxy_coords = k
        
        node_set = set(G.nodes)
        for x, y in node_set:
            l = (x - 1, y)
            r = (x + 1, y)
            u = (x, y + 1)
            d = (x, y - 1)
            for d in [l, r, u, d]:
                if d in node_set:
                    G.add_edge((x, y), d)
        
        self.oxy_coords = oxy_coords
        self.graph = G

def main():
    start = time.time()
    intcode = get_input('input.txt')
    computer = Computer(intcode)
    grid = Grid(computer)
    grid.build_grid()
    grid.build_graph()
    # print(grid.oxy_coords)

    all_paths_from_oxy = nx.algorithms.single_source_shortest_path_length(grid.graph, grid.oxy_coords)
    a1 = all_paths_from_oxy[(0, 0)]
    print("Answer to Part 1: ", a1)
    print(f"Took {time.time() - start} seconds for part 1")
    a2 = max(all_paths_from_oxy.values())
    print("Answer to Part 2: ", a2)
    print(f"Took {time.time() - start} seconds for both parts")

main()