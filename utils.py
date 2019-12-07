from collections import Counter
import networkx as nx
from typing import List


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
