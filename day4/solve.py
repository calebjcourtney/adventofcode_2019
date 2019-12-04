from collections import Counter


def has_two_adjacent_digits(text: str) -> bool:
    for x in range(10):
        if f'{x}{x}' in text:
            return True

    return False


def has_at_least_two_of_same_number(text: str) -> bool:
    return 2 in Counter(text).values()  # thanks coandco for the idea here


def string_never_decreasing(text: str) -> bool:
    for x in range(len(text) - 1):
        if text[x + 1] < text[x]:
            return False

    return True


def part_one_criteria(text: str) -> bool:
    # never decreasing runs faster, so this goes first
    if not string_never_decreasing(text):
        return False

    return has_two_adjacent_digits(text)


def part_two_criteria(text: str) -> bool:
    return has_at_least_two_of_same_number(text)


if __name__ == '__main__':
    # part one
    assert(part_one_criteria('111111'))
    assert(not part_one_criteria('223450'))
    assert(not part_one_criteria('123789'))

    part_one_passwords = []  # thanks for the idea coandco - this cuts runtime in half
    for x in range(264793, 803936):
        if part_one_criteria(str(x)):
            part_one_passwords.append(str(x))

    # part two
    assert(part_two_criteria('112233'))
    assert(not part_two_criteria('123444'))
    assert(part_two_criteria('111122'))

    count = 0
    for x in part_one_passwords:
        if part_two_criteria(x):
            count += 1

    print("part one solution:", len(part_one_passwords))
    print("part two solution:", count)
