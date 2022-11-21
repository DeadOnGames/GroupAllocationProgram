import sys
from .GenerateNeighbour import generate_neighbours
from copy import deepcopy
from statistics import mode


def Eval(node):
    return mode(map(sum, node))


def hill_climb(start_node, max_iterations=1000):
    current_node = deepcopy(start_node)
    for i in range(0, max_iterations):
        nhbrs = generate_neighbours(current_node)
        next_eval = sys.float_info.min
        next_node = None
        for node in nhbrs:
            if Eval(node) >= next_eval:
                next_eval = Eval(node)
                next_node = node
        if next_eval <= Eval(current_node):
            return current_node
        current_node = next_node
