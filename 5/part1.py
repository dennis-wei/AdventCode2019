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

def simulate(input, inst_pointer, base_input):
    print(input)
    print("inst_pointer", inst_pointer)
    code = get_padded(input[inst_pointer])
    inst_code = int(''.join(code[-2:]))
    print('code: ', inst_code)
    if inst_code == 1:
        if inst_pointer > len(input) - 5:
            print("here1")
            return
        param_1 = get_ra(code[2], input[inst_pointer + 1], input)
        param_2 = get_ra(code[1], input[inst_pointer + 2], input)
        output = input[inst_pointer + 3]
        print(output)
        print(param_1, param_2)

        input[output] = param_1 + param_2
        simulate(input, inst_pointer + 4, base_input)
    
    elif inst_code == 2:
        if inst_pointer > len(input) - 5:
            print("here2")
            return
        param_1 = get_ra(code[2], input[inst_pointer + 1], input)
        param_2 = get_ra(code[1], input[inst_pointer + 2], input)
        output = input[inst_pointer + 3]

        input[output] = param_1 * param_2
        simulate(input, inst_pointer + 4, base_input)

    elif inst_code == 99:
        print("here99")
        return

    elif inst_code == 3:
        if inst_pointer > len(input) - 2:
            print("here3")
            return
        raw_input = base_input
        param = input[inst_pointer + 1]
        input[param] = raw_input
        simulate(input, inst_pointer + 2, base_input)

    elif inst_code == 4:
        if inst_pointer > len(input) - 2:
            print("here4")
            return
        param = input[inst_pointer + 1]
        print("answer", input[param])
        simulate(input, inst_pointer + 2, base_input)

    elif inst_code == 5:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        if param1 != 0:
            inst_pointer = param2
            simulate(input, inst_pointer, base_input)
        else:
            inst_pointer += 3
            simulate(input, inst_pointer, base_input)

    elif inst_code == 6:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        if param1 == 0:
            inst_pointer = param2
            simulate(input, inst_pointer, base_input)

        else:
            inst_pointer += 3
            simulate(input, inst_pointer, base_input)

    elif inst_code == 7:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        param3 = input[inst_pointer + 3]
        if param1 < param2:
            input[param3] = 1
        else:
            input[param3] = 0
        inst_pointer += 4
        simulate(input, inst_pointer, base_input)

    elif inst_code == 8:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        param3 = input[inst_pointer + 3]
        if param1 == param2:
            input[param3] = 1
        else:
            input[param3] = 0
        inst_pointer += 4
        simulate(input, inst_pointer, base_input)

# simulate([1002, 4, 3, 4, 33], 0)
# simulate([3,9,8,9,10,9,4,9,99,-1,8], 0, 7)
simulate(problem_input, 0, 5)