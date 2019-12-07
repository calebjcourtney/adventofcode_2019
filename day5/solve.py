arg_counts = {
    1: 2,
    2: 2,
    3: 0,
    4: 1,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    99: 0
}

has_output = {
    1: True,
    2: True,
    3: True,
    4: False,
    5: False,
    6: False,
    7: True,
    8: True,
    99: False
}


def parse_modes(instruction):
    # get the modes being used
    mode = []
    mode.append(instruction % 1000 // 100)
    mode.append(instruction % 10000 // 1000)
    mode.append(instruction % 100000 // 10000)

    return mode


def op_add(loc, op_inputs, index_point):
    DATA[loc] = op_inputs[0] + op_inputs[1]
    return index_point


def op_mutliplication(loc, op_inputs, index_point):
    DATA[loc] = op_inputs[0] * op_inputs[1]
    return index_point


def op_input(loc, op_inputs, index_point):
    DATA[loc] = input_instruction
    return index_point


def op_output(loc, op_inputs, index_point):
    outputs.append(op_inputs[0])
    return index_point


def op_jumpiftrue(loc, op_inputs, index_point):
    if op_inputs[0] != 0:
        index_point = op_inputs[1]

    return index_point


def op_jumpiffalse(loc, op_inputs, index_point):
    if op_inputs[0] == 0:
        index_point = op_inputs[1]

    return index_point


def op_lessthan(loc, op_inputs, index_point):
    DATA[loc] = 1 if op_inputs[0] < op_inputs[1] else 0
    return index_point


def op_equals(loc, op_inputs, index_point):
    DATA[loc] = 1 if op_inputs[0] == op_inputs[1] else 0
    return index_point


def op_kill(loc, op_inputs, index_point):
    return None


op_function = {
    1: op_add,
    2: op_mutliplication,
    3: op_input,
    4: op_output,
    5: op_jumpiftrue,
    6: op_jumpiffalse,
    7: op_lessthan,
    8: op_equals,
    99: op_kill
}


def process_index(index_point):
    instruction = DATA[index_point]
    op_code = instruction % 100

    mode = parse_modes(instruction)

    index_point += 1

    # get the inputs for the opcode
    op_inputs = []
    for i in range(arg_counts[op_code]):
        op_inputs.append(DATA[index_point] if mode[i] == 1 else DATA[DATA[index_point]])
        index_point += 1

    loc = None

    # has an output location
    if has_output[op_code]:
        loc = DATA[index_point] if mode[-1] == 0 else None
        index_point += 1

    index_point = op_function[op_code](loc, op_inputs, index_point)

    return index_point


if __name__ == '__main__':
    # part one
    DATA = [int(val) for val in open('input.txt').read().split(',')]
    input_instruction = 1
    outputs = [0]

    index_point = 0
    while outputs[-1] == 0 and index_point is not None:
        index_point = process_index(index_point)

    print(f"part one answer: {outputs[-1]}")

    # part two
    input_instruction = 5
    outputs = [0]
    DATA = [int(val) for val in open('input.txt').read().split(',')]

    index_point = 0
    while outputs[-1] == 0 and index_point is not None:
        index_point = process_index(index_point)

    print(f"part two answer: {outputs[-1]}")
