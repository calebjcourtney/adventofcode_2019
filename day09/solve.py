from utils import IntCodeComputer


if __name__ == '__main__':
    test_1 = [int(x) for x in '1102,34915192,34915192,7,4,7,99,0'.split(',')]
    test_answer = IntCodeComputer(test_1).set_input(1).run()
    print(test_answer)
    assert(len(str(test_answer[0])) == 16)

    test_2 = [int(x) for x in '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(',')]
    test_answer = IntCodeComputer(test_2).set_input(1).run()
    print(test_answer)
    assert(test_answer[0] == 109)

    test_3 = [int(x) for x in '104,1125899906842624,99'.split(',')]
    test_answer = IntCodeComputer(test_3).set_input(1).run()
    print(test_answer)
    assert(test_answer[0] == 1125899906842624)

    data = [int(x) for x in open('input.txt', 'r').read().split(',')]

    print('start part one')
    part_one_answer = IntCodeComputer(data).set_debugger().set_input(1).run()
    print(f"part one solution: {part_one_answer}")

    print('start part two')
    part_two_answer = IntCodeComputer(data).set_debugger().set_input(2).run()
    print(f"part two solution: {part_two_answer}")
