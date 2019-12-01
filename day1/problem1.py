def get_fuel(mass):
    return (mass // 3) - 2


if __name__ == '__main__':
    assert(get_fuel(12) == 2)
    assert(get_fuel(14) == 2)
    assert(get_fuel(1969) == 654)
    assert(get_fuel(100756) == 33583)

    in_file = open('input.txt', 'r')
    masses = [int(line) for line in in_file]
    total_fuel = sum([get_fuel(mass) for mass in masses])
    print(total_fuel)
