import networkx as nx

import time

def split_orbit(orbit):
    return orbit.strip().split(')')

def get_num_orbits(o, orbits, memoized_orbits):
    if not o in orbits:
        return 0
    elif o in memoized_orbits:
        return memoized_orbits[o]

    res = get_num_orbits(orbits[o], orbits, memoized_orbits) + 1
    memoized_orbits[o] = res
    return res

with open("input.txt", 'r') as f:
    orbits = [split_orbit(o) for o in f]

with open("sample_input.txt", 'r') as f:
    sample_orbits = [split_orbit(o) for o in f]

def setup_graph(input):
    G = nx.Graph()
    orbits = {}
    for o in input:
        orbits[o[1]] = o[0]

    G.add_nodes_from(orbits.keys())

    for o1, o2 in orbits.items():
        G.add_edge(o1, o2)
        G.add_edge(o2, o1)
    return G

def main(input):
    orbits = {}
    for o in input:
        orbits[o[1]] = o[0]

    memoized_orbits = {}

    s = 0
    for o in orbits:
        s += get_num_orbits(o, orbits, memoized_orbits)
    print("Solution for Part 1: ", s)

    # G = setup_graph(input)

    # res = sum(nx.shortest_path_length(G, source=n, target="COM") for n in G.nodes())
    # print("Solution for Part 1: ", res)

# main(sample_orbits)
start = time.time()
main(orbits)
print(f'Part 1 took {time.time() - start} seconds')

with open("sample_input2.txt", 'r') as f:
    sample_orbits2 = [split_orbit(o) for o in f]

def main2(input):
    G = setup_graph(input)
    
    res = len(nx.shortest_path(G,source="SAN", target="YOU")) - 3
    print("Solution for Part 2: ", res)

# main2(sample_orbits2)
start = time.time()
main2(orbits)
print(f'Part 2 took {time.time() - start} seconds')