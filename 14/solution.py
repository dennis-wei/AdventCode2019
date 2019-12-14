import sys
import time
from collections import defaultdict
import itertools
import math
import networkx

def get_input(filename):
    with open(filename, 'r') as f:
        return f.read()

def read_input():
    return sys.stdin.read()

def get_num_material(material_string):
    l, r = material_string.split(" ")
    return (int(l), r)

def parse_cost(left):
    components = left.split(", ")
    mapping = {}
    for c in components:
        n, m = get_num_material(c)
        mapping[m] = n
    return mapping

def parse_input(filename):
    raw = get_input(filename)
    # raw = read_input()
    raw_recipes = raw.split("\n")
    recipes = [r.split(" => ") for r in raw_recipes]
    recipes = {get_num_material(r): parse_cost(l) for l, r in recipes}
    return recipes
    
def get_diff(needed, have):
    result = {}
    for k, v in needed.items():
        num_have = have.get(k, 0)
        if num_have < v:
            result[k] = v - num_have
    return result

def get_result_map(recipes):
    res = {}
    for n, m in recipes.keys():
        res[m] = max(n, res.get(m, 0))
    return res

def is_done(needed):
    for k, v in needed.items():
        if k != "ORE":
            if v > 0:
                return False
    return True

def get_next_step(recipes, res_map, num_fuel):
    needed =  { "FUEL" : num_fuel }
    # num_loops = 0
    while not is_done(needed):
        # num_loops += 1
        have = {}
        new_needed = defaultdict(int)
        for r, need in needed.items():
            if need == 0:
                continue
            if r == "ORE":
                new_needed[r] += need
                continue
            num_can_create = res_map[r]
            # print (f"Resource: {r}, Need: {need}, Can Create: {num_can_create}")
            if need > 0:
                num_iters = math.ceil(need / num_can_create)
                t = (num_can_create, r)
                # print(f"{recipes[t]} => {num_can_create}{r} | {num_iters} times")
                for resource, amount in recipes[t].items():
                    new_needed[resource] += num_iters * amount
                need -= num_iters * num_can_create
                new_needed[r] += need
            else:
                new_needed[r] += need
        needed = new_needed
        # print(needed)
        # print()

    ditems = list(needed.items())
    for k, v in ditems:
        if v == 0:
            needed.pop(k)
    return needed

def part2_driver(recipes, res_map):
    min_fuel = 0
    max_fuel = 1000000000
    while True:
        if min_fuel == max_fuel or min_fuel == max_fuel - 1:
            return min_fuel
        mid = (min_fuel + max_fuel) // 2
        num_ore_needed = get_next_step(recipes, res_map, mid).pop("ORE")
        # print(num_ore_needed)
        if num_ore_needed < 1000000000000:
            min_fuel = mid
        elif num_ore_needed > 1000000000000:
            max_fuel = mid

def main():
    start = time.time()
    recipes = parse_input('input.txt')
    possible_creations = recipes.keys()
    res_map = get_result_map(recipes)
    a1 = get_next_step(recipes, res_map, 1)["ORE"]
    print(f"Answer to Part 1: {a1}")
    print(f"Took {time.time() - start} seconds")

    start = time.time()
    a2 = part2_driver(recipes, res_map)
    print(f"Answer to Part 2: {a2}")
    print(f"Took {time.time() - start} seconds")

main()