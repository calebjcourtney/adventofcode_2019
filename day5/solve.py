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
    1: 1,
    2: 1,
    3: 1,
    4: 0,
    5: 0,
    6: 0,
    7: 1,
    8: 1,
    99: 0
}


def process_index(index_point):
    instruction = DATA[index_point]
    op_code = instruction % 100

    # get the modes being used
    mode = []
    mode.append(instruction % 1000 // 100)
    mode.append(instruction % 10000 // 1000)
    mode.append(instruction % 100000 // 10000)

    index_point += 1

    # get the inputs for the opcode
    op_inputs = []
    for i in range(arg_counts[op_code]):
        op_inputs.append(DATA[index_point] if mode[i] == 1 else DATA[DATA[index_point]])
        index_point += 1

    # has an output location
    if has_output[op_code]:
        loc = DATA[index_point] if mode[-1] == 0 else None
        index_point += 1

    if op_code == 1:
        # addition
        DATA[loc] = op_inputs[0] + op_inputs[1]

    elif op_code == 2:
        # mutliplication
        DATA[loc] = op_inputs[0] * op_inputs[1]

    elif op_code == 3:
        # input
        DATA[loc] = input_instruction

    elif op_code == 4:
        # append to outputs
        outputs.append(op_inputs[0])

    elif op_code == 5:
        # jump-if-true
        if op_inputs[0] != 0:
            index_point = op_inputs[1]

    elif op_code == 6:
        # jump-if-false
        if op_inputs[0] == 0:
            index_point = op_inputs[1]

    elif op_code == 7:
        # less than
        DATA[loc] = 1 if op_inputs[0] < op_inputs[1] else 0

    elif op_code == 8:
        # equals
        DATA[loc] = 1 if op_inputs[0] == op_inputs[1] else 0

    elif op_code == 99:
        return None

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
