def process_opcodes(num_list):
    """
    Args:
        num_list (list): List of operating codes

    Returns:
        int: the first value of the new num_list, which has been changed in the function
    """
    for count in range(len(num_list)):
        # our set of specific inputs to look at are multiples of four
        index = count * 4
        try:
            operator = num_list[index]
        except IndexError:
            # if we've gone out of the list index, then we did something wrong with the 99 index
            return num_list[0]

        if operator == 99:
            return num_list[0]

        try:
            first = num_list[index + 1]
            second = num_list[index + 2]
            replace = num_list[index + 3]
        except IndexError:
            return num_list[0]

        if operator == 1:
            # addition
            num_list[replace] = num_list[first] + num_list[second]

        elif operator == 2:
            # multiplication
            num_list[replace] = num_list[first] * num_list[second]

    # the function shouldn't make it this far
    return 0


if __name__ == '__main__':
    # check to make sure the function passes tests given in the setup
    assert(process_opcodes([1, 0, 0, 0, 99]) == 2)
    assert(process_opcodes([2, 3, 0, 3, 99]) == 2)
    assert(process_opcodes([2, 4, 4, 5, 99, 0]) == 2)
    assert(process_opcodes([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30)

    # read the data
    in_file = open('input.txt', 'r')
    num_list = [int(x) for x in in_file.read().split(',')]

    out_noun = -1
    for noun in range(99):
        for verb in range(99):
            if out_noun != -1:
                continue

            in_list = num_list[:]
            in_list[1] = noun
            in_list[2] = verb

            if process_opcodes(in_list) == 19690720:
                print(100 * noun + verb)

                out_noun = noun
                out_verb = verb

    # final check to make sure I didn't do something dumb with the array overwriting the original reference
    num_list[1] = out_noun
    num_list[2] = out_verb
    assert(process_opcodes(num_list) == 19690720)
