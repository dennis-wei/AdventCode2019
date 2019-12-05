def run_computer(input_list):
    for i in range(len(input_list) // 4):
        opcode, pos1, pos2, output_index = input_list[i * 4:i * 4 + 4]
        if opcode == 1:
            input_list[output_index] = input_list[pos1] + input_list[pos2]
        elif opcode == 2:
            input_list[output_index] = input_list[pos1] * input_list[pos2]
        elif opcode == 99:
            return
        else:
            print("unexpected opcode: ", opcode)
            raise

def run_tests():
    inputs = [
        [1, 0, 0, 0, 99],
        [2, 3, 0, 3, 99],
        [2, 4, 4, 5, 99, 0],
        [1, 1, 1, 4, 99, 5, 6, 0, 99]
    ]
    outputs = [
        [2, 0, 0, 0, 99],
        [2, 3, 0, 6, 99], 
        [2, 4, 4, 5, 99, 9801],
        [30, 1, 1, 4, 2, 5, 6, 0, 99]
    ]
    for idx, input in enumerate(inputs):
        run_computer(input)
        try:
            assert input == outputs[idx]
        except:
            print("expected: ", outputs[idx], ", got: ", input)

run_tests()

def read_input(noun, verb):
    with open('input.txt', 'r') as f:
        first_line = f.readline()
        initial_input = [int(n) for n in first_line.split(",")]
    initial_input[1] = noun
    initial_input[2] = verb
    return initial_input

input = read_input(12, 2)
run_computer(input)
print("part 1: ", input[0])

def part2():
    for i in range(100):
        for j in range(100):
            input = read_input(i, j)
            run_computer(input)
            if input[0] == 19690720:
                return 100 * i + j

print(part2())