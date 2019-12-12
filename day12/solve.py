# from copy import deepcopy
import math
from typing import List


class Moon:
    def __init__(
        self,
        x: int,
        y: int,
        z: int,
        velocity_x: int = 0,
        velocity_y: int = 0,
        velocity_z: int = 0
    ):

        self.x = x
        self.y = y
        self.z = z

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z

    def shift_moon(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.z += self.velocity_z

    def calculate_potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def calculate_kinetic_energy(self):
        return abs(self.velocity_x) + abs(self.velocity_y) + abs(self.velocity_z)

    def calculate_total_energy(self):
        return self.calculate_potential_energy() * self.calculate_kinetic_energy()


def apply_gravity(moon_a, moon_b):
    # change x values
    if moon_a.x > moon_b.x:
        moon_a.velocity_x -= 1
        moon_b.velocity_x += 1

    elif moon_a.x < moon_b.x:
        moon_a.velocity_x += 1
        moon_b.velocity_x -= 1

    # change y values
    if moon_a.y > moon_b.y:
        moon_a.velocity_y -= 1
        moon_b.velocity_y += 1

    elif moon_a.y < moon_b.y:
        moon_a.velocity_y += 1
        moon_b.velocity_y -= 1

    # change z values
    if moon_a.z > moon_b.z:
        moon_a.velocity_z -= 1
        moon_b.velocity_z += 1

    elif moon_a.z < moon_b.z:
        moon_a.velocity_z += 1
        moon_b.velocity_z -= 1


def step(moons: List[Moon]) -> List[Moon]:
    pairs = [
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3),
        (2, 3)
    ]

    # calculate the velocities
    for pair in pairs:
        a, b = pair
        apply_gravity(moons[a], moons[b])

    # apply those velocities
    for moon in moons:
        moon.shift_moon()

    return moons


def part_one_solution(moons):
    for _ in range(1000):
        moons = step(moons)

    total_energy = 0
    for moon in moons:
        total_energy += moon.calculate_total_energy()

    return total_energy


def least_common_multiple(x, y):
    return x // math.gcd(x, y) * y


def part_two_solution(moons):
    seen_x, seen_y, seen_z = set(), set(), set()
    repeat_x, repeat_y, repeat_z = None, None, None
    time = 0

    while True:
        if repeat_x is not None and repeat_y is not None and repeat_z is not None:
            break

        moons = step(moons)

        if repeat_x is None:
            check_x = str([[moon.x, moon.velocity_x] for moon in moons])
            if check_x in seen_x:
                repeat_x = time

            seen_x.add(check_x)

        if repeat_y is None:
            check_y = str([[moon.y, moon.velocity_y] for moon in moons])
            if check_y in seen_y:
                repeat_y = time

            seen_y.add(check_y)

        if repeat_z is None:
            check_z = str([[moon.z, moon.velocity_z] for moon in moons])
            if check_z in seen_z:
                repeat_z = time

            seen_z.add(check_z)

        time += 1

    return least_common_multiple(least_common_multiple(repeat_x, repeat_y), repeat_z)


if __name__ == "__main__":
    """
    <x=7, y=10, z=17>
    <x=-2, y=7, z=0>
    <x=12, y=5, z=12>
    <x=5, y=-8, z=6>
    """

    moons = [Moon(7, 10, 17), Moon(-2, 7, 0), Moon(12, 5, 12), Moon(5, -8, 6)]

    print(f"part one solution: {part_one_solution(moons)}")
    print(f"part two solution: {part_two_solution(moons)}")
