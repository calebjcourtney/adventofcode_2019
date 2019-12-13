from collections import Counter, defaultdict
import networkx as nx
from typing import List
from enum import Enum
import math


def read_data() -> str:
    return open('input.txt', 'r').read()


# DAY 1 #
def get_recursive_fuel(mass: int) -> int:
    # from day 1, calculates the fuel (recursively) required based on mass size given
    fuel = (mass // 3) - 2
    return 0 if fuel < 0 else fuel + get_recursive_fuel(fuel)


#### DAY 4 ####
def has_adjacent_characters(text: str, count: int = 2) -> bool:
    # checks to see if there are two characters next to each other
    c = "".join([key for key, value in Counter(text).items() if value == count])
    for x in c:
        if x * count in text:
            return True

    return False


def has_exactly_count(text: str, count: int) -> bool:
    # checks a string for if character occurs count times
    return count in Counter(text).values()  # thanks coandco for the idea here


def string_never_decreasing(text: str) -> bool:
    # checks to see if the text of a string is always increasing
    for x in range(len(text) - 1):
        if text[x + 1] < text[x]:
            return False

    return True


###### DAY 6 ######
def count_orbit_connections(input_data: List[List]):
    graph = nx.DiGraph()
    graph.add_edges_from(input_data)

    orbit_count = sum([predecessor_count(node, graph) for node in graph.nodes])

    return orbit_count


def predecessor_count(node, graph) -> int:
    predecessors = list(graph.predecessors(node))
    predecessors_sum = len(predecessors)

    # recursion actually worked on this problem!
    return sum([predecessors_sum + predecessor_count(pred, graph) for pred in predecessors])


def get_distance_between_objects(input_data: List[List], first_object: str, second_object: str) -> int:
    graph = nx.Graph()
    graph.add_edges_from(input_data)

    path = nx.shortest_path(graph, first_object, second_object)

    return len(path)


########## DAY 10 ##########
def get_angle(point_one, point_two):
    return math.degrees(math.atan2(point_one.x - point_two.x, point_one.y - point_two.y) % (2 * math.pi))


def get_distance(point_one, point_two):
    return math.sqrt((point_one.x - point_two.x) ** 2 + (point_one.y - point_two.y) ** 2)


############ DAY 12 ############
def least_common_multiple(x, y):
    return x // math.gcd(x, y) * y


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

    def calculate_potential_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def calculate_kinetic_energy(self) -> int:
        return abs(self.velocity_x) + abs(self.velocity_y) + abs(self.velocity_z)

    def calculate_total_energy(self) -> int:
        return self.calculate_potential_energy() * self.calculate_kinetic_energy()

    @staticmethod
    def apply_gravity(moon_a, moon_b) -> None:
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


############### DAYS 2, 5, 7, 9, 11 - will probably be heavily used ################
class State(Enum):
    INIT = 1
    LIVE = 2
    HALT = 99


class IntCodeComputer:
    def __init__(self, codes: List) -> None:
        self.code = defaultdict(int, enumerate(codes))  # thanks Peter200lx
        self.inputs = []
        self.default_input = 0
        self.outputs = []
        self.cursorPos = 0
        self.debug = False
        self.modes = []
        self.relativebase = 0
        self.opmapping = {
            1: self.op_add,
            2: self.op_mutliplication,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jumpiftrue,
            6: self.op_jumpiffalse,
            7: self.op_lessthan,
            8: self.op_equals,
            9: self.op_relativebase,
            99: self.op_kill
        }
        self.state = State.INIT

    def input(self, in_value: int):
        # this allows for multiple inputs into the program, which will be used and removed one by one
        self.inputs.append(in_value)
        return self

    def set_input(self, in_value: int):
        # this allows for multiple inputs into the program
        self.default_input = in_value
        return self

    def _inc(self, i: int = 1) -> None:
        self.cursorPos += i

    def set_debugger(self, debug: bool = True):
        self.debug = debug
        return self

    def debug_print(self, op_name, message) -> None:
        if self.debug and op_name == 'output':
            print(f"{self.cursorPos - 1}: {op_name} -> {message}")

    def _next_instruction(self):
        instruction = self.code[self.cursorPos]
        modes, opcode = divmod(instruction, 100)
        self.modes = [int(x) for x in reversed(str(modes))]

        self._inc()

        return opcode

    def _next_mode(self):
        if len(self.modes) > 0:
            return self.modes.pop(0)
        return 0

    def _get_parameter(self):
        value = self.code[self.cursorPos]
        mode = self._next_mode()

        # Position Mode
        if mode == 0:
            value = self.code[value]
        # Immediate Mode
        elif mode == 1:
            pass
        elif mode == 2:
            value = self.code[self.relativebase + value]
        else:
            raise Exception(f"Invalid Mode: {mode}")

        self._inc()
        return value

    def _get_dest_parameter(self):
        value = self.code[self.cursorPos]
        mode = self._next_mode()  # Throw away
        if mode == 1:
            raise Exception(f"Mode for get dest parameter {mode}")

        self._inc()

        value += (self.relativebase if mode == 2 else 0)

        return value

    def run(self) -> int or None:
        if self.state == State.LIVE:
            raise Exception("This is already live. What are you doing?")

        self.state = State.LIVE
        while self.state == State.LIVE:
            op = self._next_instruction()

            if op in self.opmapping:
                self.opmapping[op]()

            else:
                print(f"unknown opcode {op} at cursorPos {self.cursorPos - 1}: {self.code[self.cursorPos - 1]}")
                print(self.code)
                return None

        return self.outputs

    def op_add(self) -> None:
        arg1 = self._get_parameter()
        arg2 = self._get_parameter()
        pos = self._get_dest_parameter()

        self.debug_print('add', f"value({self.code[pos]}) in pos({pos}) -> {arg1 + arg2}")

        self.code[pos] = arg1 + arg2

    def op_mutliplication(self) -> None:
        arg1 = self._get_parameter()
        arg2 = self._get_parameter()
        pos = self._get_dest_parameter()

        self.debug_print('multiply', f"value({self.code[pos]}) in pos({pos}) -> {arg1 * arg2}")

        self.code[pos] = arg1 * arg2

    def op_input(self) -> None:
        pos = self._get_dest_parameter()

        try:
            new_val = self.inputs.pop(0)
        except IndexError:
            new_val = self.default_input

        self.code[pos] = new_val

        self.debug_print('input', f"pos({pos}) = {self.code[pos]}")

    def op_output(self) -> int:
        output_val = self._get_parameter()

        self.debug_print('output', f"adding({output_val}) to last item in outputs")

        self.outputs.append(output_val)

    def op_jumpiftrue(self) -> None:
        arg1 = self._get_parameter()
        arg2 = self._get_parameter()

        if arg1 == 1:
            self.cursorPos = arg2

    def op_jumpiffalse(self) -> None:
        arg1 = self._get_parameter()
        arg2 = self._get_parameter()

        if arg1 == 0:
            self.cursorPos = arg2

    def op_lessthan(self) -> None:
        arg1 = self._get_parameter()
        arg2 = self._get_parameter()
        pos = self._get_dest_parameter()

        self.code[pos] = 1 if arg1 < arg2 else 0

    def op_equals(self) -> None:
        arg1 = self._get_parameter()
        arg2 = self._get_parameter()
        pos = self._get_dest_parameter()

        self.code[pos] = 1 if arg1 == arg2 else 0

    def op_relativebase(self):
        arg1 = self._get_parameter()

        self.debug_print('relativebase', f"modifying relbase value({self.relativebase}) -> {self.relativebase + arg1}")
        self.relativebase += arg1

    def op_kill(self):
        self.debug_print("kill", "killing the computer")
        self.state = State.HALT


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


########################## TESTS ##########################
def test_recursivefuel():
    assert(get_recursive_fuel(12) == 2)
    assert(get_recursive_fuel(14) == 2)
    assert(get_recursive_fuel(1969) == 966)
    assert(get_recursive_fuel(100756) == 50346)


def test_adjacent_characters():
    assert(has_adjacent_characters('free') is True)
    assert(has_adjacent_characters('free', 3) is False)


def test_stringdecreasing():
    assert(string_never_decreasing('free') is False)
    assert(string_never_decreasing('abc') is True)
    assert(string_never_decreasing('123abc') is True)


def test_countorbitconn():
    day6_sample = [
        ["COM", "B"],
        ["B", "C"],
        ["C", "D"],
        ["D", "E"],
        ["E", "F"],
        ["B", "G"],
        ["G", "H"],
        ["D", "I"],
        ["E", "J"],
        ["J", "K"],
        ["K", "L"]
    ]
    assert(count_orbit_connections(day6_sample) == 42)


def test_distancebetweenobjects():
    day6_sample = [
        ["COM", "B"],
        ["B", "C"],
        ["C", "D"],
        ["D", "E"],
        ["E", "F"],
        ["B", "G"],
        ["G", "H"],
        ["D", "I"],
        ["E", "J"],
        ["J", "K"],
        ["K", "L"],
        ["K", "YOU"],
        ["I", "SAN"]
    ]
    assert(get_distance_between_objects(day6_sample, "YOU", "SAN") == 7)


def test_intcodecomputer():
    sample1 = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 33, 37, 225, 101, 6, 218, 224, 1001, 224, -82, 224, 4, 224, 102, 8, 223, 223, 101, 7, 224, 224, 1, 223, 224, 223, 1102, 87, 62, 225, 1102, 75, 65, 224, 1001, 224, -4875, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 1102, 49, 27, 225, 1101, 6, 9, 225, 2, 69, 118, 224, 101, -300, 224, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 224, 223, 223, 1101, 76, 37, 224, 1001, 224, -113, 224, 4, 224, 1002, 223, 8, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1101, 47, 50, 225, 102, 43, 165, 224, 1001, 224, -473, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 3, 224, 1, 224, 223, 223, 1002, 39, 86, 224, 101, -7482, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 6, 224, 1, 223, 224, 223, 1102, 11, 82, 225, 1, 213, 65, 224, 1001, 224, -102, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 6, 224, 1, 224, 223, 223, 1001, 14, 83, 224, 1001, 224, -120, 224, 4, 224, 1002, 223, 8, 223, 101, 1, 224, 224, 1, 223, 224, 223, 1102, 53, 39, 225, 1101, 65, 76, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 1107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 329, 101, 1, 223, 223, 8, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 1001, 223, 1, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 359, 1001, 223, 1, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 374, 1001, 223, 1, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 389, 101, 1, 223, 223, 7, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 404, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 419, 101, 1, 223, 223, 107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 434, 101, 1, 223, 223, 7, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 449, 101, 1, 223, 223, 108, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 464, 101, 1, 223, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 479, 101, 1, 223, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 494, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 509, 101, 1, 223, 223, 1007, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 524, 1001, 223, 1, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 539, 1001, 223, 1, 223, 1107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 554, 1001, 223, 1, 223, 1007, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 569, 1001, 223, 1, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 584, 1001, 223, 1, 223, 108, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 599, 1001, 223, 1, 223, 8, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 614, 1001, 223, 1, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 629, 1001, 223, 1, 223, 8, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 644, 1001, 223, 1, 223, 1108, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 659, 101, 1, 223, 223, 107, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226]
    result = IntCodeComputer(sample1).set_input(1).run()
    assert(result[-1] == 16209841)

    # result = IntCodeComputer(sample1).set_input(5).run()
    # assert(result[-1] == 8834787)

    sample2 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    result = IntCodeComputer(sample2).set_input(1).run()
    for x in range(len(sample2)):
        assert(result[x] == sample2[x])

    sample3 = [1102, 34463338, 34463338, 63, 1007, 63, 34463338, 63, 1005, 63, 53, 1101, 3, 0, 1000, 109, 988, 209, 12, 9, 1000, 209, 6, 209, 3, 203, 0, 1008, 1000, 1, 63, 1005, 63, 65, 1008, 1000, 2, 63, 1005, 63, 904, 1008, 1000, 0, 63, 1005, 63, 58, 4, 25, 104, 0, 99, 4, 0, 104, 0, 99, 4, 17, 104, 0, 99, 0, 0, 1101, 25, 0, 1016, 1102, 760, 1, 1023, 1102, 1, 20, 1003, 1102, 1, 22, 1015, 1102, 1, 34, 1000, 1101, 0, 32, 1006, 1101, 21, 0, 1017, 1102, 39, 1, 1010, 1101, 30, 0, 1005, 1101, 0, 1, 1021, 1101, 0, 0, 1020, 1102, 1, 35, 1007, 1102, 1, 23, 1014, 1102, 1, 29, 1019, 1101, 767, 0, 1022, 1102, 216, 1, 1025, 1102, 38, 1, 1011, 1101, 778, 0, 1029, 1102, 1, 31, 1009, 1101, 0, 28, 1004, 1101, 33, 0, 1008, 1102, 1, 444, 1027, 1102, 221, 1, 1024, 1102, 1, 451, 1026, 1101, 787, 0, 1028, 1101, 27, 0, 1018, 1101, 0, 24, 1013, 1102, 26, 1, 1012, 1101, 0, 36, 1002, 1102, 37, 1, 1001, 109, 28, 21101, 40, 0, -9, 1008, 1019, 41, 63, 1005, 63, 205, 1001, 64, 1, 64, 1105, 1, 207, 4, 187, 1002, 64, 2, 64, 109, -9, 2105, 1, 5, 4, 213, 1106, 0, 225, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -9, 1206, 10, 243, 4, 231, 1001, 64, 1, 64, 1105, 1, 243, 1002, 64, 2, 64, 109, -3, 1208, 2, 31, 63, 1005, 63, 261, 4, 249, 1106, 0, 265, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 5, 21108, 41, 41, 0, 1005, 1012, 287, 4, 271, 1001, 64, 1, 64, 1105, 1, 287, 1002, 64, 2, 64, 109, 6, 21102, 42, 1, -5, 1008, 1013, 45, 63, 1005, 63, 307, 1105, 1, 313, 4, 293, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -9, 1201, 0, 0, 63, 1008, 63, 29, 63, 1005, 63, 333, 1106, 0, 339, 4, 319, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -13, 2102, 1, 4, 63, 1008, 63, 34, 63, 1005, 63, 361, 4, 345, 1105, 1, 365, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 5, 1201, 7, 0, 63, 1008, 63, 33, 63, 1005, 63, 387, 4, 371, 1105, 1, 391, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 7, 1202, 1, 1, 63, 1008, 63, 32, 63, 1005, 63, 411, 1105, 1, 417, 4, 397, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 20, 1205, -7, 431, 4, 423, 1106, 0, 435, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 2, 2106, 0, -3, 1001, 64, 1, 64, 1105, 1, 453, 4, 441, 1002, 64, 2, 64, 109, -7, 21101, 43, 0, -9, 1008, 1014, 43, 63, 1005, 63, 479, 4, 459, 1001, 64, 1, 64, 1105, 1, 479, 1002, 64, 2, 64, 109, -5, 21108, 44, 43, 0, 1005, 1018, 495, 1105, 1, 501, 4, 485, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -7, 1205, 9, 517, 1001, 64, 1, 64, 1105, 1, 519, 4, 507, 1002, 64, 2, 64, 109, 11, 1206, -1, 531, 1106, 0, 537, 4, 525, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -15, 1208, 0, 36, 63, 1005, 63, 557, 1001, 64, 1, 64, 1106, 0, 559, 4, 543, 1002, 64, 2, 64, 109, 7, 2101, 0, -7, 63, 1008, 63, 35, 63, 1005, 63, 581, 4, 565, 1106, 0, 585, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -3, 21107, 45, 46, 4, 1005, 1015, 607, 4, 591, 1001, 64, 1, 64, 1105, 1, 607, 1002, 64, 2, 64, 109, -16, 2102, 1, 10, 63, 1008, 63, 31, 63, 1005, 63, 631, 1001, 64, 1, 64, 1106, 0, 633, 4, 613, 1002, 64, 2, 64, 109, 1, 2107, 33, 10, 63, 1005, 63, 649, 1106, 0, 655, 4, 639, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 17, 2101, 0, -9, 63, 1008, 63, 31, 63, 1005, 63, 679, 1001, 64, 1, 64, 1106, 0, 681, 4, 661, 1002, 64, 2, 64, 109, -6, 2107, 34, 0, 63, 1005, 63, 703, 4, 687, 1001, 64, 1, 64, 1106, 0, 703, 1002, 64, 2, 64, 109, 5, 1207, -5, 34, 63, 1005, 63, 719, 1105, 1, 725, 4, 709, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -15, 1202, 6, 1, 63, 1008, 63, 20, 63, 1005, 63, 751, 4, 731, 1001, 64, 1, 64, 1105, 1, 751, 1002, 64, 2, 64, 109, 21, 2105, 1, 5, 1001, 64, 1, 64, 1106, 0, 769, 4, 757, 1002, 64, 2, 64, 109, 5, 2106, 0, 5, 4, 775, 1001, 64, 1, 64, 1106, 0, 787, 1002, 64, 2, 64, 109, -27, 1207, 4, 35, 63, 1005, 63, 809, 4, 793, 1001, 64, 1, 64, 1106, 0, 809, 1002, 64, 2, 64, 109, 13, 2108, 33, -1, 63, 1005, 63, 831, 4, 815, 1001, 64, 1, 64, 1106, 0, 831, 1002, 64, 2, 64, 109, 4, 21107, 46, 45, 1, 1005, 1014, 851, 1001, 64, 1, 64, 1105, 1, 853, 4, 837, 1002, 64, 2, 64, 109, 3, 21102, 47, 1, -3, 1008, 1013, 47, 63, 1005, 63, 875, 4, 859, 1106, 0, 879, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -9, 2108, 28, 2, 63, 1005, 63, 895, 1106, 0, 901, 4, 885, 1001, 64, 1, 64, 4, 64, 99, 21101, 27, 0, 1, 21102, 1, 915, 0, 1106, 0, 922, 21201, 1, 59074, 1, 204, 1, 99, 109, 3, 1207, -2, 3, 63, 1005, 63, 964, 21201, -2, -1, 1, 21102, 942, 1, 0, 1105, 1, 922, 21201, 1, 0, -1, 21201, -2, -3, 1, 21102, 1, 957, 0, 1105, 1, 922, 22201, 1, -1, -2, 1106, 0, 968, 22102, 1, -2, -2, 109, -3, 2105, 1, 0]
    result = IntCodeComputer(sample3).set_input(1).run()
    print(result)
    assert(result[-1] == 3518157894)
