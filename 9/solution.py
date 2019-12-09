import time

with open('input.txt', 'r') as f:
    line = f.read().strip()
    problem_input = [int(n) for n in line.split(',')]

# with open('sample_input1.txt', 'r') as f:
#     line = f.read().strip()
#     problem_input = [int(n) for n in line.split(',')]

def get_num_digits(n):
    return len(str(n))

def get_padded(n):
    return list(str(n).zfill(5))

class Computer:
    def __init__(self, program, input):
        self.program = program
        self.program.extend(0 for n in range(1000))
        self.pc = 0
        self.relative_base = 0
        self.halted = False
        self.input = input
        self.output = []

    def get_ra(self, mode, param):
        if int(mode) == 0:
            return self.program[param]
        elif int(mode) == 1:
            return param
        elif int(mode) == 2:
            return self.program[param + self.relative_base]
        else:
            raise f"Unknown mode: {int(mode)}"
    
    def get_output_index(self, mode, param):
        # print("mode: ", mode)
        if int(mode) == 0 or int(mode) == 1:
            return param
        elif int(mode) == 2:
            return self.relative_base + param
        else:
            raise f"Unknown mode: {int(mode)}"

    def simulate(self):
        if self.halted:
            return
        # print([e for e in enumerate(self.program)])
        # print("pc", self.pc)
        code = get_padded(self.program[self.pc])
        inst_code = int(''.join(code[-2:]))
        # print('code: ', code)
        # print('inst_code: ', inst_code)
        if inst_code == 1:
            param_1 = self.get_ra(code[2], self.program[self.pc + 1])
            param_2 = self.get_ra(code[1], self.program[self.pc + 2])
            param3 = self.get_output_index(code[0], self.program[self.pc + 3])
            # print(f"adding {param_1} and {param_2} and setting to index {param3}")

            self.program[param3] = param_1 + param_2
            self.pc += 4
        
        elif inst_code == 2:
            param_1 = self.get_ra(code[2], self.program[self.pc + 1])
            param_2 = self.get_ra(code[1], self.program[self.pc + 2])
            param3 = self.get_output_index(code[0], self.program[self.pc + 3])

            # print(f"multiplying {param_1} and {param_2} and setting to index {param3}")

            self.program[param3] = param_1 * param_2
            self.pc += 4

        elif inst_code == 99:
            # print("here99")
            self.halted = True

        elif inst_code == 3:
            if self.input != None:
                param = self.get_output_index(code[2], self.program[self.pc + 1])
                # print(f"Setting {self.input} in index {param}")
                self.program[param] = self.input
                self.input = None
                self.pc += 2
            else:
                raise "Expected Input"

        elif inst_code == 4:
            param = self.get_ra(code[2], self.program[self.pc + 1])
            # print("output param: ", param)
            self.output.append(param)
            self.pc += 2

        elif inst_code == 5:
            param1 = self.get_ra(code[2], self.program[self.pc + 1])
            param2 = self.get_ra(code[1], self.program[self.pc + 2])
            # print(f"Jumping if {param1} is not 0 to {param2}")
            if param1 != 0:
                self.pc = param2
            else:
                self.pc += 3

        elif inst_code == 6:
            param1 = self.get_ra(code[2], self.program[self.pc + 1])
            param2 = self.get_ra(code[1], self.program[self.pc + 2])
            # print(f"Jumping if {param1} is 0 to {param2}")
            if param1 == 0:
                self.pc = param2
            else:
                self.pc += 3

        elif inst_code == 7:
            param1 = self.get_ra(code[2], self.program[self.pc + 1])
            param2 = self.get_ra(code[1], self.program[self.pc + 2])
            param3 = self.get_output_index(code[0], self.program[self.pc + 3])
            # print(f"Setting {param3} to 1 if {param1} < {param2}")
            if param1 < param2:
                self.program[param3] = 1
            else:
                self.program[param3] = 0
            self.pc += 4

        elif inst_code == 8:
            param1 = self.get_ra(code[2], self.program[self.pc + 1])
            param2 = self.get_ra(code[1], self.program[self.pc + 2])
            param3 = self.get_output_index(code[0], self.program[self.pc + 3])
            # print(f"Setting {param3} to 1 if {param1} == {param2}")
            if param1 == param2:
                self.program[param3] = 1
            else:
                self.program[param3] = 0
            self.pc += 4
        
        elif inst_code == 9:
            param = self.get_ra(code[2], self.program[self.pc + 1])
            # print("setting relative_base to: ", self.relative_base + param)
            self.relative_base += param
            self.pc += 2
    
    def run_simulation(self):
        while not self.halted:
            self.simulate()
        return self.output

computer = Computer(problem_input, 1)
start = time.time()
output = computer.run_simulation()
print("Solution to Part 1: ", output)
print(f"Took {time.time() - start} seconds")

computer = Computer(problem_input, 2)
start = time.time()
output = computer.run_simulation()
print("Solution to Part 2: ", output)
print(f"Took {time.time() - start} seconds")