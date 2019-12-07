import itertools

import time

with open('input.txt', 'r') as f:
    line = f.read().strip()
    problem_input = [int(n) for n in line.split(',')]

def get_num_digits(n):
    return len(str(n))

def get_padded(n):
    return list(str(n).zfill(5))

def get_ra(mode, param, input):
    if int(mode) == 0:
        return input[param]
    elif int(mode) == 1:
        return param
    else:
        raise f"Unknown mode: {int(mode)}"

def simulate(input, inst_pointer, base_input, base_idx):
    # print([e for e in enumerate(input)])
    # print("inst_pointer", inst_pointer)
    code = get_padded(input[inst_pointer])
    inst_code = int(''.join(code[-2:]))
    # print('code: ', inst_code)
    if inst_code == 1:
        if inst_pointer > len(input) - 5:
            # print("here1")
            return
        param_1 = get_ra(code[2], input[inst_pointer + 1], input)
        param_2 = get_ra(code[1], input[inst_pointer + 2], input)
        output = input[inst_pointer + 3]
        # print(f"adding {param_1} and {param_2} and setting to index {output}")

        input[output] = param_1 + param_2
        return simulate(input, inst_pointer + 4, base_input, base_idx)
    
    elif inst_code == 2:
        if inst_pointer > len(input) - 5:
            # print("here2")
            return
        param_1 = get_ra(code[2], input[inst_pointer + 1], input)
        param_2 = get_ra(code[1], input[inst_pointer + 2], input)
        output = input[inst_pointer + 3]

        # print(f"multiplying {param_1} and {param_2} and setting to index {output}")

        input[output] = param_1 * param_2
        return simulate(input, inst_pointer + 4, base_input, base_idx)

    elif inst_code == 99:
        # print("here99")
        return

    elif inst_code == 3:
        if inst_pointer > len(input) - 2:
            # print("here3")
            return
        raw_input = base_input[base_idx]
        param = input[inst_pointer + 1]
        # print(f"Setting {base_input[base_idx]} in index {param}")
        input[param] = raw_input
        return simulate(input, inst_pointer + 2, base_input, base_idx + 1)

    elif inst_code == 4:
        if inst_pointer > len(input) - 2:
            # print("here4")
            return
        param = input[inst_pointer + 1]
        # print("answer", input[param])
        # print()
        return input[param]

    elif inst_code == 5:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        if param1 != 0:
            inst_pointer = param2
            return simulate(input, inst_pointer, base_input, base_idx)
        else:
            inst_pointer += 3
            return simulate(input, inst_pointer, base_input, base_idx)

    elif inst_code == 6:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        if param1 == 0:
            inst_pointer = param2
            return simulate(input, inst_pointer, base_input, base_idx)

        else:
            inst_pointer += 3
            return simulate(input, inst_pointer, base_input, base_idx)

    elif inst_code == 7:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        param3 = input[inst_pointer + 3]
        if param1 < param2:
            input[param3] = 1
        else:
            input[param3] = 0
        inst_pointer += 4
        return simulate(input, inst_pointer, base_input, base_idx)

    elif inst_code == 8:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        param3 = input[inst_pointer + 3]
        if param1 == param2:
            input[param3] = 1
        else:
            input[param3] = 0
        inst_pointer += 4
        return simulate(input, inst_pointer, base_input, base_idx)

# simulate([1002, 4, 3, 4, 33], 0)
# simulate([3,9,8,9,10,9,4,9,99,-1,8], 0, 7)
# simulate(problem_input, 0, 5)

def simulate_amplitude(problem_input):
    max_so_far = 0
    for perm in itertools.permutations([0, 1, 2, 3, 4]):
        # print("trying permutation: ", perm)
        # print("AMP 1")
        output1 = simulate(problem_input.copy(), 0, [perm[0], 0], 0)
        # print("AMP 2")
        output2 = simulate(problem_input.copy(), 0, [perm[1], output1], 0)
        # print("AMP 3")
        output3 = simulate(problem_input.copy(), 0, [perm[2], output2], 0)
        # print("AMP 4")
        output4 = simulate(problem_input.copy(), 0, [perm[3], output3], 0)
        # print("AMP 5")
        output5 = simulate(problem_input.copy(), 0, [perm[4], output4], 0)
        if output5 > max_so_far:
            max_so_far = output5
            best_perm_so_far = perm
    
    print("Solution to Part 1: ", max_so_far)
    print("    Permutation: ", best_perm_so_far)

# simulate_amplitude([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
# simulate_amplitude([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
# simulate_amplitude([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])

start = time.time()
simulate_amplitude(problem_input)
print(f'Part 1 took {time.time() - start} seconds')
