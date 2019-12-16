import math
import time

def parse_input(filename):
    with open(filename, 'r') as f:
        return [int(s) for s in f.read().strip()]

def part1(inp, num_loops):
    inp = inp
    print(len(inp))
    for loop_num in range(num_loops):
        if len(inp) % 10 == 0:
            print("loop_num: ", loop_num)
        acc = []
        # print(f"BEGIN: {inp}")
        inp.insert(0, 0)
        # print(f"0 INSERTED: {inp}")
        for j in range(1, len(inp)):
            if j * 3 > len(inp):
                sli = inp[j:2*j][-10:]
                acc.append(sum(sli) % 10)
                continue
            s = 0
            pos_offset = j
            neg_offset = 3 * j
            while pos_offset < len(inp) or neg_offset < len(inp):
                # print(f"pos: {pos_offset}, neg: {neg_offset}")
                # print(f"pos slice: {inp[pos_offset:pos_offset + j]}")
                # print(f"neg slice: {inp[neg_offset:neg_offset + j]}")
                s += sum(inp[pos_offset:pos_offset + j])
                s -= sum(inp[neg_offset:neg_offset + j])
                pos_offset += 4 * j
                neg_offset += 4 * j
            # print("res: ", abs(s) % 10)
            acc.append(abs(s) % 10)
        inp = acc
        # print(inp)
        # print()
    return "".join(str(n) for n in inp)

def part2_driver(inp, offset):
    # offset = 4
    # print("Input length: ", len(inp))
    short = inp[offset:]
    for loop_num in range(100):
        # print(short[-5:])
        # if loop_num % 1 == 0:
            # print("loop_num: ", loop_num)
        acc = []
        s = 0
        for j in range(len(short) - 1, -1, -1):
            s = (s + short[j]) % 10
            acc.append(s)
        short = acc[::-1]
    # print(short)
    # return "".join([str(n) for n in short[:4]])
    return "".join([str(n) for n in short[:8]])


def part2(filename):
    raw_inp = parse_input(filename)
    offset = int("".join(str(n) for n in raw_inp[:7]))
    print("offset: ", offset)
    inp = raw_inp * 10000
    full = part2_driver(inp, offset)
    return full


start = time.time()
a1 = part1(parse_input('input.txt'), 4)[:8]
print(f"Answer to Part 1 is {a1}")
print(f"Took {time.time() - start} seconds")

a2 = part2('input.txt')
print(f"Answer to Part 2 is {a2}")
print(f"Took {time.time() - start} seconds total")