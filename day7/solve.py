#!/usr/bin/env python3

import itertools

from utils import IntCodeComputer


def amplify(codes):
    max_output = 0

    for sequence in itertools.permutations(list(range(5))):
        signal = 0

        for phase in sequence:
            comp = IntCodeComputer(codes).input(phase)
            comp.secondary_input = signal
            signal = comp.run()

        if signal > max_output:
            max_output = signal

    return max_output


def feedback(codes):
    max_output = 0

    for sequence in itertools.permutations(list(range(5, 10))):
        result = 0

        loop = [IntCodeComputer(codes).input(phase) for phase in sequence]

        while result is not None:
            for amplifier in loop:
                signal = result
                amplifier.secondary_input = signal
                result = amplifier.run()
                if result is None:
                    break

        if signal > max_output:
            max_output = signal

    return max_output


def run():
    input_file = open('input.txt', 'r')

    codes = [int(x) for x in input_file.read().split(",")]

    output = amplify(codes)
    print(f"Part one solution: {output}")

    output = feedback(codes)
    print(f"Part two solution: {output}")


if __name__ == '__main__':
    run()
