def is_valid(n):
    digits = [int(x) for x in list(str(n))]
    digit_count_sequence = []
    curr_count = 1
    for i in range(len(digits) - 1):
        if digits[i] > digits[i + 1]:
            return False

        if digits[i] == digits[i + 1]:
            curr_count += 1
        else:
            digit_count_sequence.append(curr_count)
            curr_count = 1
    digit_count_sequence.append(curr_count)
    return 2 in digit_count_sequence

def tests():
    assert is_valid(112233) == True
    assert is_valid(123444) == False
    assert is_valid(111122) == True

tests()

def main():
    ret = sum(is_valid(n) for n in range(206938, 679128))
    print(ret)

main()