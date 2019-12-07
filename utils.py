from collections import Counter
import networkx as nx
from typing import List


# DAY 1 #
def get_recursive_fuel(mass):
    # from day 1, calculates the fuel (recursively) required based on mass size given
    fuel = (mass // 3) - 2
    return 0 if fuel < 0 else fuel + get_recursive_fuel(fuel)


#### DAY 4 ####
def has_two_adjacent_digits(text: str) -> bool:
    # from day 4 - checks to see if there are two digits next to each other
    for x in range(10):
        if f'{x}{x}' in text:
            return True

    return False


def has_exactly_count(text: str, count: int) -> bool:
    # checks a string for if a number occurs more than once
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
