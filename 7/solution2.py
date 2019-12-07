import itertools

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

def simulate(input, inst_pointer, new_input):
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
        return simulate(input, inst_pointer + 4, new_input)
    
    elif inst_code == 2:
        if inst_pointer > len(input) - 5:
            # print("here2")
            return
        param_1 = get_ra(code[2], input[inst_pointer + 1], input)
        param_2 = get_ra(code[1], input[inst_pointer + 2], input)
        output = input[inst_pointer + 3]

        # print(f"multiplying {param_1} and {param_2} and setting to index {output}")

        input[output] = param_1 * param_2
        return simulate(input, inst_pointer + 4, new_input)

    elif inst_code == 99:
        # print("here99")
        return "HALTED", inst_pointer, None, new_input

    elif inst_code == 3:
        if inst_pointer > len(input) - 2:
            # print("here3")
            return
        if new_input != None:
            raw_input = new_input
            param = input[inst_pointer + 1]
            # print(f"Setting {new_input} in index {param}")
            input[param] = raw_input
            return simulate(input, inst_pointer + 2, None)
        else:
            return "AWAITING_INPUT", inst_pointer, None, new_input

    elif inst_code == 4:
        if inst_pointer > len(input) - 2:
            # print("here4")
            return
        param = input[inst_pointer + 1]
        return "OUTPUT", inst_pointer + 2, input[param], new_input

    elif inst_code == 5:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        if param1 != 0:
            inst_pointer = param2
            return simulate(input, inst_pointer, new_input)
        else:
            inst_pointer += 3
            return simulate(input, inst_pointer, new_input)

    elif inst_code == 6:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        if param1 == 0:
            inst_pointer = param2
            return simulate(input, inst_pointer, new_input)

        else:
            inst_pointer += 3
            return simulate(input, inst_pointer, new_input)

    elif inst_code == 7:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        param3 = input[inst_pointer + 3]
        if param1 < param2:
            input[param3] = 1
        else:
            input[param3] = 0
        inst_pointer += 4
        return simulate(input, inst_pointer, new_input)

    elif inst_code == 8:
        param1 = get_ra(code[2], input[inst_pointer + 1], input)
        param2 = get_ra(code[1], input[inst_pointer + 2], input)
        param3 = input[inst_pointer + 3]
        if param1 == param2:
            input[param3] = 1
        else:
            input[param3] = 0
        inst_pointer += 4
        return simulate(input, inst_pointer, new_input)

class Amp:
    def __init__(self, num, input_queue, program):
        self.num = num
        self.inst_pointer = 0
        self.input_queue = input_queue
        self.input_idx = 0
        self.program = program
        self.output_queue = []
        self.latest_output = None
        self.halted = False
    
    def simulate_on_input(self, inp):
        status, latest_inst_pointer, latest_output, latest_input = simulate(self.program, self.inst_pointer, inp)
        self.inst_pointer = latest_inst_pointer
        if status == "HALTED":
            # print(f"Halting AMP {self.num}")
            self.halted = True
        elif status == "OUTPUT":
            # print(f"AMP {self.num} output {latest_output}")
            self.output_queue.append(latest_output)
            self.latest_output = latest_output
            if latest_input:
                self.simulate_on_input(self.program, self.inst_pointer, latest_input)
        # elif status == "AWAITING_INPUT":
        #     print(f"Awaiting input at instruciton pointer {latest_inst_pointer}")
        
    def receive_input(self, input):
        self.input_queue.extend(input)
    
    def flush_output(self):
        temp = self.output_queue.copy()
        self.output_queue = []
        return temp
    
    def simulate_while_input(self):
        # print()
        # print(f"Simulating AMP {self.num}")
        while(len(self.input_queue) > 0) and not self.halted:
            next_input = self.input_queue.pop(0)
            # print(f"Simulating AMP {self.num} on input {next_input}")
            res = self.simulate_on_input(next_input)

def all_halted(amps):
    return all(a.halted or len(a.input_queue) == 0 for a in amps)

def simulate_loop(problem_input):
    max_so_far = 0
    best_perm_so_far = None
    for perm in itertools.permutations([5, 6, 7, 8, 9]):
        print("Trying perm: ", perm)
        a1 = Amp(0, [perm[0], 0], problem_input.copy())
        a2 = Amp(1, [perm[1]], problem_input.copy())
        a3 = Amp(2, [perm[2]], problem_input.copy())
        a4 = Amp(3, [perm[3]], problem_input.copy())
        a5 = Amp(4, [perm[4]], problem_input.copy())
        amps = [a1, a2, a3, a4, a5]

        curr_amp_idx = 0
        while not all_halted(amps):
            curr_amp = amps[curr_amp_idx]
            curr_amp.simulate_while_input()
            next_amp_idx = (curr_amp_idx + 1) % 5
            amps[next_amp_idx].receive_input(curr_amp.flush_output())
            curr_amp_idx = next_amp_idx
        # for amp in amps:
        #     print(amp.halted, amp.input_queue)
        # print("Final AMP5 output: ", amps[4].latest_output)
        if amps[4].latest_output > max_so_far:
            max_so_far = amps[4].latest_output
            best_perm_so_far = perm
    print("Solution for Part 2: ", max_so_far)
    print("    on permutation: ", best_perm_so_far)


# simulate_loop([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
# simulate_loop([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
simulate_loop(problem_input)