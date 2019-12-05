def get_fuel(n):
    return n // 3 - 2

def run_tests():
    test_cases = [12, 14, 1969, 100756]
    solutions = [2, 2, 654, 33583]
    for i in range(4):
        try:
            assert(get_fuel(test_cases[i]) == solutions[i])

        except:
            print(get_fuel(test_cases[i]))

run_tests()

def read_input():
    with open('input.txt', 'r') as f:
        return [int(l) for l in f]

def sum_fuel():
    input = read_input()
    s = sum(get_fuel(n) for n in input)
    print(s)

sum_fuel()