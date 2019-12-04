def has_two_adjacent_digits(text):
    for x in range(10):
        if '{}{}'.format(x, x) in text:
            return True

    return False


def has_only_two_adjacents(text):
    for x in range(10):
        if '{}{}'.format(x, x) in text and '{}{}{}'.format(x, x, x) not in text:
            return True

    return False


def never_decreasing(text):
    for x in range(len(text) - 1):
        if text[x + 1] < text[x]:
            return False

    return True


def part_one_criteria(text):
    if not has_two_adjacent_digits(text):
        return False

    if not never_decreasing(text):
        return False

    return True


def part_two_criteria(text):
    if not has_only_two_adjacents(text):
        return False

    if not never_decreasing(text):
        return False

    return True


if __name__ == '__main__':
    # part one
    assert(part_one_criteria('111111'))
    assert(not part_one_criteria('223450'))
    assert(not part_one_criteria('123789'))

    count = 0

    for x in range(264793, 803936):
        if part_one_criteria(str(x)):
            count += 1

    print("part one:", count)

    # part two
    assert(part_two_criteria('112233'))
    assert(not part_two_criteria('123444'))
    assert(part_two_criteria('111122'))

    count = 0

    for x in range(264793, 803936):
        if part_two_criteria(str(x)):
            count += 1

    print("part two:", count)
