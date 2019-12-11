import sys
import math
import time
import inflect

start = time.time()
with open('input.txt', 'r') as f:
    input = f.read()
print(input)
print()

p = inflect.engine()

def get_asteroids(grid):
    asteroids = set()
    for height in range(len(grid)):
        for width in range(len(grid[height])):
            if grid[height][width] == '#':
                asteroids.add((height, width))
    return asteroids

def get_num_in_sight(grid, asteroids, coord):
    slopes = {}
    for x, y in asteroids:
        if (x, y) == coord:
            continue
        mx, my = (x - coord[0], y - coord[1])
        # print(mx, my)
        while math.gcd(mx, my) != 1:
            d = math.gcd(mx, my)
            mx //= d
            my //= d
        slopes[(x, y)] = (mx, my)
        # print("slope added")

    # print(f"slopes for {coord}: {slopes}")
    return(len(set(slopes.values())))

def build_grid(input):
    grid = list(list(l) for l in input.split("\n"))
    # for height in range(len(grid)):
    #     for width in range(len(grid[height])):
        #     print(grid[height][width], end="")
        # print("")
    return grid

grid = build_grid(input)
asteroids = get_asteroids(grid)
# print(asteroids)
# print()

# best = 0
# for height in range(len(grid)):
#     for width in range(len(grid[height])):
#         if grid[width][height] != '#':
#             num_in_sight = get_num_in_sight(grid, asteroids, (width, height))
#             best = max(num_in_sight, best)

best = 0
best_coord = None
for height in range(len(grid)):
    for width in range(len(grid[height])):
        if grid[height][width] == '#':
            num_in_sight = get_num_in_sight(grid, asteroids, (height, width))
            best = max(num_in_sight, best)
            if best == num_in_sight:
                best_coord = (height, width)

print(f"Solution to Part 1: {best_coord[::-1]} with {best} visible")
print(f"Took {time.time() - start} seconds")

def get_dist(c1, c2):
    # print(c1, c2)
    return (c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2

def get_angle(mx, my):
    angle = (math.degrees(math.atan2(my, mx)) - 180) % 360
    if angle == 0:
        return 360
    return angle

def destroy_visible(grid, asteroids, coord, num_destroyed = 0):
    inv_slopes = {}
    if len(asteroids) == 0:
        return
    for x, y in asteroids:
        if (x, y) == coord:
            continue
        mx, my = (x - coord[0], y - coord[1])
        # print(mx, my)
        while math.gcd(mx, my) != 1:
            d = math.gcd(mx, my)
            mx //= d
            my //= d
        inv_slopes[(mx, my)] = min((x, y), inv_slopes.get((mx, my), (math.inf, math.inf)), key = lambda c: get_dist(c, coord))

    # print("length of inv_slopes: ", len(inv_slopes))
    visible = sorted(inv_slopes.items(), key=lambda c: get_angle(*c[0]))[::-1]
    # print(list((v[1], get_angle(*v[0])) for v in visible[:10]))
    for v in visible:
        num_destroyed += 1
        if num_destroyed in [1, 2, 3, 10, 20, 50, 100, 199, 200]:
            print(f"The {p.ordinal(num_destroyed)} asteroid is {v[1][::-1]}")
        if num_destroyed == 200:
            return v[1][::-1]
        asteroids.remove(v[1])
    if num_destroyed < 200:
        return destroy_visible(grid, asteroids, coord, num_destroyed)

start = time.time()
destroyed = destroy_visible(grid, asteroids, best_coord)
print("Solution to Part 2 ", destroyed[0] * 100 + destroyed[1])
print(f"Took {time.time() - start} seconds")
