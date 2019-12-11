import networkx as nx


def part_one(input_data):
    graph_part_one = nx.DiGraph()
    graph_part_one.add_edges_from(input_data)

    orbit_count = sum([get_pred_sum(node, graph_part_one) for node in graph_part_one.nodes])

    return orbit_count


def get_pred_sum(node, graph_part_one):
    predecessors = list(graph_part_one.predecessors(node))
    predecessors_sum = len(predecessors)

    # recursion actually worked on this problem!
    return sum([predecessors_sum + get_pred_sum(pred, graph_part_one) for pred in predecessors])


def part_two(input_data):
    graph_part_two = nx.Graph()
    graph_part_two.add_edges_from(input_data)

    path = nx.shortest_path(graph_part_two, 'YOU', 'SAN')

    return len(path[2:-1])


if __name__ == '__main__':
    DATA = [[record.split(')')[0], record.split(')')[1]] for record in open('input.txt', 'r').read().split('\n')]

    print(f"part one solution: {part_one(DATA)}")
    print(f"part two solution: {part_two(DATA)}")
