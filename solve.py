import utils


def solve_part_one():
    pass


def solve_part_two():
    pass


if __name__ == '__main__':
    # part one
    example_1, example_2, example_3 = "", "", ""
    answer_1, answer_2, answer_3 = "", "", ""

    assert(solve_part_one(example_1) == answer_1)
    assert(solve_part_one(example_2) == answer_2)
    assert(solve_part_one(example_3) == answer_3)

    DATA = open('input.txt', 'r').read()
    print(f"part 1 answer: {solve_part_one(DATA)}")

    # part two
    example_1, example_2, example_3 = "", "", ""
    answer_1, answer_2, answer_3 = "", "", ""
    assert(solve_part_two(example_1) == answer_1)
    assert(solve_part_two(example_2) == answer_2)
    assert(solve_part_two(example_3) == answer_3)

    DATA = open('input.txt', 'r').read()
    print(f"part 2 answer: {solve_part_two(DATA)}")
