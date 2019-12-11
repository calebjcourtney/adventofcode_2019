from collections import Counter


def solve_part_one(data):
    split_data = [data[(25 * 6 * x):(25 * 6 * (x + 1))] for x in range(int(len(data) / (25 * 6)))]
    output = 0
    zero_count = None

    for section in split_data:
        c = Counter(section)
        if zero_count is None:
            zero_count = c['0']
            output = c['1'] * c['2']

        elif c['0'] < zero_count:
            zero_count = c['0']
            output = c['1'] * c['2']

    return output


def solve_part_two(data):
    split_data = [data[(25 * 6 * x):(25 * 6 * (x + 1))] for x in range(int(len(data) / (25 * 6)))]
    output_layer = ''
    for x in range(len(split_data[0])):
        for layer in split_data:
            if layer[x] in ['1', '0']:
                output_layer += layer[x]
                break
            else:
                continue

    second_split = [output_layer[25 * x: 25 * (x + 1)].replace('1', '#').replace('0', ' ') for x in range(6)]

    for line in second_split:
        print(line)


if __name__ == '__main__':
    DATA = open('input.txt', 'r').read()
    print(f"part 1 answer: {solve_part_one(DATA)}")

    solve_part_two(DATA)
