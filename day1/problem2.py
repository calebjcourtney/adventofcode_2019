import math


def get_recursive_fuel(mass):
    fuel = math.floor(mass / 3) - 2
    if fuel < 0:
        return 0

    else:
        return fuel + get_recursive_fuel(fuel)


if __name__ == '__main__':
    assert(get_recursive_fuel(12) == 2)
    assert(get_recursive_fuel(14) == 2)
    assert(get_recursive_fuel(1969) == 966)
    assert(get_recursive_fuel(100756) == 50346)

    in_file = open('input.txt', 'r')
    masses = [int(line) for line in in_file]

    total_fuel = sum([get_recursive_fuel(mass) for mass in masses])
    print(total_fuel)
