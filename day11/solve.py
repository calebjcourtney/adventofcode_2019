from utils import IntCodeComputer, State, read_data

BLACK = 0
WHITE = 1

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class PaintingBot(IntCodeComputer):
    """docstring for PaintingBot"""

    def run(self) -> int or None:
        self.state = State.LIVE
        while len(self.outputs) < 2:
            op = self._next_instruction()

            if op in self.opmapping:
                self.opmapping[op]()

            else:
                print(f"unknown opcode {op} at cursorPos {self.cursorPos - 1}: {self.code[self.cursorPos - 1]}")
                print(self.code)
                return None

        return self.outputs


def solve_part_one(data):
    program = PaintingBot(data).set_debugger()

    grid = {}
    x = 0
    y = 0
    facing = UP

    first = True

    while program.state != State.HALT:
        color = grid[(x, y)] if (x, y) in grid else WHITE if first else BLACK
        first = False

        program.default_input = color

        new_color, turn = program.run()

        program.default_input = new_color
        program.outputs = []

        grid[(x, y)] = new_color

        facing = (facing + (3 if turn == 0 else 1)) % 4  # this was a find on reddit from user mikedoug
        if facing == UP:
            y += 1
        elif facing == DOWN:
            y -= 1
        elif facing == LEFT:
            x -= 1
        else:
            x += 1

    return grid


def solve_part_two(grid):
    minx = min([x[0] for x in grid])
    miny = min([y[1] for y in grid])
    maxx = max([x[0] for x in grid])
    maxy = max([y[1] for y in grid])

    print('Stage two:')
    for y in range(maxy, miny - 1, -1):
        line = ""
        for x in range(minx - 2, maxx + 2):
            if (x, y) in grid and grid[(x, y)] == WHITE:
                line += "X"
            else:
                line += " "

        print(line)


if __name__ == '__main__':
    DATA = [int(x) for x in read_data().split(',')]
    grid = solve_part_one(DATA)
    print(grid)
    print(f"solution one: {len(grid)}")

    solve_part_two(grid)
