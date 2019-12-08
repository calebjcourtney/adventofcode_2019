import itertools
from utils import IntCodeComputer


def part_one_solution(codes):
    max_output = 0

    for sequence in itertools.permutations(list(range(5))):
        result = 0

        loop = [IntCodeComputer(codes).input(phase) for phase in sequence]

        while result is not None:
            for amplifier in loop:
                signal = result
                amplifier.secondary_input = signal
                result = amplifier.run()
                if result is None:
                    break

            if signal > max_output:
                max_output = signal

    return max_output


def part_two_solution(codes):
    max_output = 0

    for sequence in itertools.permutations(list(range(5, 10))):
        result = 0

        loop = [IntCodeComputer(codes).input(phase) for phase in sequence]

        while result is not None:
            for amplifier in loop:
                signal = result
                amplifier.secondary_input = signal
                result = amplifier.run()
                if result is None:
                    break

            if signal > max_output:
                max_output = signal

    return max_output


if __name__ == '__main__':
    test_1 = [int(x) for x in "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(',')]
    answer_1 = 43210
    assert(part_one_solution(test_1) == answer_1)

    test_2 = [int(x) for x in "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0".split(',')]
    answer_2 = 54321
    assert(part_one_solution(test_2) == answer_2)

    test_3 = [int(x) for x in "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0".split(',')]
    answer_3 = 65210
    assert(part_one_solution(test_3) == answer_3)

    input_file = open('input.txt', 'r')
    codes = [int(x) for x in input_file.read().split(",")]

    output = part_one_solution(codes)
    print(f"Part one solution: {output}")

    test_4 = [int(x) for x in "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(',')]
    asnwer_4 = 139629729
    assert(part_two_solution(test_4) == asnwer_4)

    test_5 = [int(x) for x in "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(',')]
    answer_5 = 18216
    assert(part_two_solution(test_5) == answer_5)

    output = part_two_solution(codes)
    print(f"Part two solution: {output}")
