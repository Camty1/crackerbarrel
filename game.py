import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self):
        self.adjacency_list = {}
        self.visual = []
        self.edge_labels = {}

    def add_node(self, node):
        if not node in self.adjacency_list:
            self.adjacency_list[node] = set()

    def add_edge(self, edge, move=None):
        self.add_node(edge[0])
        self.add_node(edge[1])
        self.adjacency_list[edge[0]].add(edge[1])
        self.visual.append(edge)
        if move:
            self.edge_labels[edge] = move

    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


class Board:

    def __init__(self, side_length: int = 5, missing_peg: int = 0):
        assert 3 <= side_length
        self.side_length = side_length
        self.num_pegs = sum(list(range(side_length + 1)))

        assert 0 <= missing_peg < self.num_pegs
        self.pegs = [True] * self.num_pegs
        self.pegs[missing_peg] = False

    def draw_board(self):
        counter = 0
        character_width = int(np.log10(self.num_pegs - 1)) + 1
        for i in range(self.side_length):
            print(" " * (character_width) * (self.side_length - 1 - i), end="")
            for j in range(i + 1):
                if self.pegs[counter]:
                    print("\033[92m", end="")
                else:
                    print("\033[91m", end="")

                print(
                    f"{counter:0{character_width}}" + " " * (character_width),
                    end="",
                )
                counter += 1

            print("\033[0m")

    def get_position(self, index):
        if index < 0:
            return None

        row = 0
        while index - (row + 1) >= 0 and row < self.side_length:
            row += 1
            index -= row

        if row == self.side_length:
            return None

        return (row, index)

    def get_index(self, position):
        if position[1] > position[0]:
            return None
        if position[0] < 0 or position[0] >= self.side_length:
            return None
        if position[1] < 0 or position[1] >= self.side_length:
            return None

        return sum(list(range(position[0] + 1))) + position[1]

    def get_valid_moves(self):
        valid_moves = []
        for i in range(self.num_pegs):
            if not self.pegs[i]:
                position = self.get_position(i)

                above_left_2 = (position[0] - 2, position[1] - 2)
                above_left_2_idx = self.get_index(above_left_2)

                if above_left_2_idx != None and self.pegs[above_left_2_idx]:
                    above_left_1 = (position[0] - 1, position[1] - 1)
                    above_left_1_idx = self.get_index(above_left_1)

                    if self.pegs[above_left_1_idx]:
                        valid_moves.append((above_left_2_idx, i))

                above_right_2 = (position[0] - 2, position[1])
                above_right_2_idx = self.get_index(above_right_2)

                if above_right_2_idx != None and self.pegs[above_right_2_idx]:
                    above_right_1 = (position[0] - 1, position[1])
                    above_right_1_idx = self.get_index(above_right_1)

                    if self.pegs[above_right_1_idx]:
                        valid_moves.append((above_right_2_idx, i))

                below_left_2 = (position[0] + 2, position[1] + 2)
                below_left_2_idx = self.get_index(below_left_2)

                if below_left_2_idx != None and self.pegs[below_left_2_idx]:
                    below_left_1 = (position[0] + 1, position[1] + 1)
                    below_left_1_idx = self.get_index(below_left_1)

                    if self.pegs[below_left_1_idx]:
                        valid_moves.append((below_left_2_idx, i))

                below_right_2 = (position[0] + 2, position[1])
                below_right_2_idx = self.get_index(below_right_2)

                if below_right_2_idx != None and self.pegs[below_right_2_idx]:
                    below_right_1 = (position[0] + 1, position[1])
                    below_right_1_idx = self.get_index(below_right_1)

                    if self.pegs[below_right_1_idx]:
                        valid_moves.append((below_right_2_idx, i))

                left_2 = (position[0], position[1] - 2)
                left_2_idx = self.get_index(left_2)

                if left_2_idx != None and self.pegs[left_2_idx]:
                    left_1 = (position[0], position[1] - 1)
                    left_1_idx = self.get_index(left_1)

                    if self.pegs[left_1_idx]:
                        valid_moves.append((left_2_idx, i))

                right_2 = (position[0], position[1] + 2)
                right_2_idx = self.get_index(right_2)

                if right_2_idx != None and self.pegs[right_2_idx]:
                    right_1 = (position[0], position[1] + 1)
                    right_1_idx = self.get_index(right_1)

                    if self.pegs[right_1_idx]:
                        valid_moves.append((right_2_idx, i))

        return valid_moves

    def move_pegs(self, move):
        assert move in self.get_valid_moves()

        start_idx = move[0]
        start_pos = self.get_position(start_idx)
        assert start_pos

        end_idx = move[1]
        end_pos = self.get_position(end_idx)
        assert end_pos

        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        remove_pos = (start_pos[0] + dx // 2, start_pos[1] + dy // 2)
        remove_idx = self.get_index(remove_pos)
        assert remove_idx

        self.pegs[start_idx] = False
        self.pegs[remove_idx] = False
        self.pegs[end_idx] = True


def generate_graph(side_length: int = 5, missing_peg: int = 3):
    board = Board(side_length=side_length, missing_peg=missing_peg)
    graph = Graph()
    visited = set()
    queue = [tuple(board.pegs)]
    prev = {}

    while queue:
        state = queue.pop(0)
        board.pegs = list(state)
        moves = board.get_valid_moves()

        for move in moves:
            board.move_pegs(move)
            new_state = tuple(board.pegs)
            if not new_state in visited:
                visited.add(new_state)
                prev[new_state] = state
                graph.add_edge((state, new_state), move)
                queue.append(new_state)
            board.pegs = list(state)

    return graph, prev
