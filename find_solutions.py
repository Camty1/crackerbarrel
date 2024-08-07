#!.venv/bin/python3
import numpy as np
from game import Board, Graph, generate_graph
import time
import os

side_length = 5
board = Board(side_length)
for i in range(board.num_pegs):
    graph, prev = generate_graph(side_length, i)

    num_sols = 0
    for j in range(board.num_pegs):
        x = [False] * board.num_pegs
        x[j] = True
        node = tuple(x)
        if node in prev:
            num_sols += 1

    print(f"{i:02}: {num_sols} solutions")


for i in range(board.num_pegs):
    x = [False] * board.num_pegs
    x[i] = True
    node = tuple(x)
    if node in prev:
        input("Next solution (Enter to start): ")
        sequence = []
        sequence.append(node)
        while node in prev:
            sequence.append(prev[node])
            node = prev[node]

        sequence = reversed(sequence)
        board = Board()
        for state in sequence:

            os.system("clear")
            board.pegs = list(state)
            board.draw_board()
            time.sleep(1)
