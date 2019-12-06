def get_points_steps(in_text: str, point = None) -> tuple:
    points = []
    steps = 0
    cursor = [0, 0]

    for code in in_text.split(','):
        if (cursor[0], cursor[1]) == point:
            break

        if code[0] == 'R':
            for x in range(int(code[1:])):
                cursor[0] += 1
                points.append((cursor[0], cursor[1]))
                steps += 1

                if (cursor[0], cursor[1]) == point:
                    break

        elif code[0] == 'L':
            for x in range(int(code[1:])):
                cursor[0] -= 1
                points.append((cursor[0], cursor[1]))
                steps += 1

                if (cursor[0], cursor[1]) == point:
                    break

        elif code[0] == 'U':
            for x in range(int(code[1:])):
                cursor[1] += 1
                points.append((cursor[0], cursor[1]))
                steps += 1

                if (cursor[0], cursor[1]) == point:
                    break

        elif code[0] == 'D':
            for x in range(int(code[1:])):
                cursor[1] -= 1
                points.append((cursor[0], cursor[1]))
                steps += 1

                if (cursor[0], cursor[1]) == point:
                    break

        if (cursor[0], cursor[1]) == point:
            break

    return set(points), steps


def get_intersect_steps(in_text: str, point = None) -> tuple:
    first_points, first_steps = get_points_steps(in_text[0], point)
    second_points, second_steps = get_points_steps(in_text[1], point)

    return (list(first_points & second_points), first_steps + second_steps)


def get_part_one(in_text: str) -> int:
    intersections, steps = get_intersect_steps(in_text)
    return min([abs(x[0]) + abs(x[1]) for x in intersections])


def get_part_two(in_text: str) -> int:
    intersections, steps = get_intersect_steps(in_text)
    return min([get_intersect_steps(in_text, intersect)[1] for intersect in intersections])


if __name__ == '__main__':
    # read the data
    in_file = open('input.txt', 'r')
    data = [x for x in in_file.read().split('\n')]

    # part one
    assert(get_part_one(['R8,U5,L5,D3', 'U7,R6,D4,L4']) == 6)
    assert(get_part_one(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]) == 159)
    assert(get_part_one(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]) == 135)
    print(get_part_one(data))

    # part two
    assert(get_part_two(['R8,U5,L5,D3', 'U7,R6,D4,L4']) == 30)
    assert(get_part_two(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]) == 610)
    assert(get_part_two(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]) == 410)
    print(get_part_two(data))
