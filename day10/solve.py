import math
import itertools
from collections import namedtuple, defaultdict


Point = namedtuple("Point", "x y")


def read(file):
    with open(file, "r") as f:
        return [
            Point(x, y)
            for y, line in enumerate(f.readlines())
            for x, c in enumerate(line) if c == "#"
        ]


def get_angle(point_one, point_two):
    return math.degrees(math.atan2(point_one.x - point_two.x, point_one.y - point_two.y) % (2 * math.pi))


def solve_part_one(asteroids):
    angles = defaultdict(set)

    for a1 in asteroids:
        for a2 in asteroids:
            if a1 == a2:
                continue

            angles[a1].add(get_angle(a1, a2))

    base = None
    angle_count = 0
    for coords, angle_items in angles.items():
        if len(angle_items) > angle_count:
            base = coords
            angle_count = len(angle_items)

    return base, angle_count


def get_distance(point_one, point_two):
    return math.sqrt((point_one.x - point_two.x) ** 2 + (point_one.y - point_two.y) ** 2)


def solve_part_two(base, asteroids):
    asteroids.remove(base)

    angles = defaultdict(list)
    for asteroid in asteroids:
        angle = 360 - get_angle(base, asteroid)

        if angle == 360:
            angle = 0

        angles[angle].append(asteroid)

    sort_by_angle = [angles[angle] for angle in sorted(angles.keys())]

    # sort so final asteroid in sublist is nearest
    for asteroids in sort_by_angle:
        asteroids.sort(key=lambda a: get_distance(base, a), reverse=True)

    destroyed = 0
    for angle in itertools.cycle(sort_by_angle):
        if angle:
            asteroid = angle.pop()
            destroyed += 1

            if destroyed == 200:
                return asteroid.x * 100 + asteroid.y


if __name__ == '__main__':
    asteroids = read("input.txt")
    base, answer_1 = solve_part_one(asteroids)
    print(f"part 1 answer: {answer_1}")
    print(f"part 2 answer: {solve_part_two(base, asteroids)}")
