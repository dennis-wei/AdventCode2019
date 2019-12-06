from collections import defaultdict
import networkx as nx

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

def main(input):
    orbits = {}
    for o in input:
        orbits[o[1]] = o[0]

    memoized_orbits = defaultdict(int)

    sum = 0
    for o in orbits:
        sum += get_num_orbits(o, orbits, memoized_orbits)
    print(orbits)
    print(memoized_orbits)
    print(sum)

# main(sample_orbits)
# main(orbits)

with open("sample_input2.txt", 'r') as f:
    sample_orbits2 = [split_orbit(o) for o in f]

def main2(input):
    G = nx.Graph()
    orbits = {}
    for o in input:
        orbits[o[1]] = o[0]

    G.add_nodes_from(orbits.keys())

    for o1, o2 in orbits.items():
        G.add_edge(o1, o2)
        G.add_edge(o2, o1)
    
    print(len(nx.shortest_path(G,source="SAN", target="YOU")) - 3)

main2(sample_orbits2)
main2(orbits)
