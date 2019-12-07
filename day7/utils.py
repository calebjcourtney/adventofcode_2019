from collections import Counter
import networkx as nx
from typing import List, Dict, Tuple, Sequence, Mapping


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


############### DAYS 2, 5, 7 - will probably be heavily used ################
class IntCodeComputer:
    def __init__(self, codes):
        self.code = [x for x in codes]
        self.inputs = []
        self.secondary_input = 0
        self.outputs = []
        self.cursorPos = 0
        self.modes = []
        self.opmapping = {  # note that 4 is missing
            1: self.op_add,
            2: self.op_mutliplication,
            3: self.op_input,
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

            if op == 4:
                return self.op_output()

            elif op == 99:
                return None

        return None

    def op_add(self):
        arg1, arg2, pos = self.code[self.cursorPos:self.cursorPos + 3]
        self.code[pos] = self.value(arg1, self.modes[0]) + self.value(arg2, self.modes[1])
        self.cursorPos += 3

    def op_mutliplication(self):
        arg1, arg2, pos = self.code[self.cursorPos:self.cursorPos + 3]
        self.code[pos] = self.value(arg1, self.modes[0]) * self.value(arg2, self.modes[1])
        self.cursorPos += 3

    def op_input(self):
        pos = self.code[self.cursorPos]
        try:
            self.code[pos] = self.inputs.pop(0)  # this was taken from  Peter200lx who had the inputs `pop` each time
        except IndexError:
            self.code[pos] = self.secondary_input

        self.cursorPos += 1

    def op_output(self):
        pos = self.code[self.cursorPos]
        return self.value(pos, self.modes[0])

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
