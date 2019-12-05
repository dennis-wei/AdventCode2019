def get_fuel(n, acc):
    additional = n // 3 - 2
    if additional > 0:
        return get_fuel(additional, acc + additional)

    return acc

def run_tests():
    test_cases = [12, 14, 1969, 100756]
    solutions = [2, 2, 966, 50346]
    for i in range(4):
        fuel = get_fuel(test_cases[i], 0)
        try:
            assert(fuel == solutions[i])

        except:
            print("expected: ", solutions[i], ", got: ", fuel)

run_tests()

def read_input():
    with open('input.txt', 'r') as f:
        return [int(l) for l in f]

def sum_fuel():
    input = read_input()
    s = sum(get_fuel(n, 0) for n in input)
    print(s)

sum_fuel()