import time

with open('input.txt', 'r') as f:
    input = [int(n) for n in f.read().strip()]

start = time.time()
per_layer = 25 * 6
layers = [input[i:i+per_layer] for i in range(0, len(input), per_layer)]

def count_num(layer, num):
    return sum(n == num for n in layer)

num_zeros = [count_num(l, 0) for l in layers]
best_layer = min(enumerate(num_zeros), key = lambda x: x[1])[0]

answ = count_num(layers[best_layer], 1) * count_num(layers[best_layer], 2)
print(f"Solution to Part 1: {answ}")
print(f"Took {time.time() - start} seconds to complete")

start = time.time()
def apply_layer(layers):
    if layers[0] != 2:
        return layers[0]
    return apply_layer(layers[1:])

zipped_layers = list(zip(*layers))

combined = list(apply_layer(p) for p in zipped_layers)

encoding = {1: "#", 0: " ", 2: "#"}

def format(layer):
    rows = [layer[i:i+25] for i in range(0, len(layer), 25)]
    for r in rows:
        print("".join(encoding[n] for n in r))

print("Solution to Part 2")
format(combined)
print(f"Took {time.time() - start} seconds to complete")