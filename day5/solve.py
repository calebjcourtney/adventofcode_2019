class IntCodeComputer:
    def __init__(self, codes):
        self.code = [x for x in codes]
        self.inputs = []
        self.outputs = []
        self.cursorPos = 0
        self.modes = []
        self.opmapping = {
            1: self.op_add,
            2: self.op_mutliplication,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jumpiftrue,
            6: self.op_jumpiffalse,
            7: self.op_lessthan,
            8: self.op_equals
        }

    def value(self, arg, mode):
        return arg if mode else self.code[arg]

    def input(self, input):
        # this allows for multiple inputs into the program
        self.inputs.append(input)
        return self

    def run(self):
        while True:
            mode, op = divmod(self.code[self.cursorPos], 100)
            self.cursorPos += 1

            self.modes = [int(x) for x in reversed(str(mode))] + [0, 0, 0]

            if op in self.opmapping:
                self.opmapping[op]()

            # opcode 99: halt
            elif op == 99:
                break

        return self.outputs[-1]

    def op_add(self):
        # opcode 1: add(arg1, arg2) -> arg3
        arg1, arg2, pos = self.code[self.cursorPos:self.cursorPos + 3]
        self.code[pos] = self.value(arg1, self.modes[0]) + self.value(arg2, self.modes[1])
        self.cursorPos += 3

    def op_mutliplication(self):
        # opcode 2: multiply(arg1, arg2) -> arg2
        arg1, arg2, pos = self.code[self.cursorPos:self.cursorPos + 3]
        self.code[pos] = self.value(arg1, self.modes[0]) * self.value(arg2, self.modes[1])
        self.cursorPos += 3

    def op_input(self):
        # opcode 2: multiply(arg1, arg2) -> arg2
        pos = self.code[self.cursorPos]
        self.code[pos] = self.inputs.pop(0)  # this was taken from  Peter200lx who had the inputs `pop` each time
        self.cursorPos += 1

    def op_output(self):
        pos = self.code[self.cursorPos]
        self.outputs.append(self.value(pos, self.modes[0]))
        self.cursorPos += 1

    def op_jumpiftrue(self):
        arg1, arg2 = self.code[self.cursorPos:self.cursorPos + 2]
        self.cursorPos += 2

        if self.value(arg1, self.modes[0]) != 0:
            self.cursorPos = self.value(arg2, self.modes[1])

    def op_jumpiffalse(self):
        arg1, arg2 = self.code[self.cursorPos:self.cursorPos + 2]
        self.cursorPos += 2

        if self.value(arg1, self.modes[0]) == 0:
            self.cursorPos = self.value(arg2, self.modes[1])

    def op_lessthan(self):
        arg1, arg2, pos = self.code[self.cursorPos:self.cursorPos + 3]
        self.code[pos] = 1 if self.value(arg1, self.modes[0]) < self.value(arg2, self.modes[1]) else 0
        self.cursorPos += 3

    def op_equals(self):
        arg1, arg2, pos = self.code[self.cursorPos:self.cursorPos + 3]
        self.code[pos] = 1 if self.value(arg1, self.modes[0]) == self.value(arg2, self.modes[1]) else 0
        self.cursorPos += 3


def run():
    input_file = open('input.txt', 'r')
    codes = [int(x) for x in input_file.read().split(",")]

    signal = IntCodeComputer(codes).input(1).run()
    print(f"first solution: {signal}")

    signal = IntCodeComputer(codes).input(5).run()
    print(f"first solution: {signal}")


if __name__ == '__main__':
    run()
