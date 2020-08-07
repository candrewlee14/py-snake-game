from settings import *

def add_with_wrap(num, multiplier):
    return (num + multiplier * CELL_SIZE) % SCREEN_SIZE

class Node():
    def __init__(self, pos: tuple, ref: Node):
        self.pos = pos
        self.prev = ref

class Autopilot():
    def get_pre_path(self, )
    def get_minimum_long_path(self, current_pos, occupied_cells):
        q = []
        


    def _add_neighbors(self, current_node: Node, q: list, occupied_cells: set):
        current_pos = current_node.pos
        neighbors = set()
        #right
        neighbors.add(tuple(current_pos[0], add_with_wrap(current_pos[1], 1)))
        #left
        neighbors.add(tuple(current_pos[0], add_with_wrap(current_pos[1], -1)))
        #top
        neighbors.add(tuple(add_with_wrap(current_pos[0], -1), current_pos[1]))
        #bottom
        neighbors.add(tuple(add_with_wrap(current_pos[0], 1), current_pos[1]))

        neighbors.difference_update(occupied_cells)
        q.extend(list(neighbors))
