import sys
from .GenerateNeighbour import generate_neighbours
from copy import deepcopy


def hill_climb(start_node, EVAL_HILL_CLIMB, max_iterations=10):
    current_node = deepcopy(start_node)
    for i in range(0, max_iterations):
        nhbrs = generate_neighbours(current_node)
        next_eval = EVAL_HILL_CLIMB(current_node)
        next_node = deepcopy(current_node)
        for node in nhbrs:
            if EVAL_HILL_CLIMB(node) >= next_eval:
                next_eval = EVAL_HILL_CLIMB(node)
                next_node = node
        if next_eval <= EVAL_HILL_CLIMB(current_node):
            return current_node
        current_node = next_node
    return current_node
