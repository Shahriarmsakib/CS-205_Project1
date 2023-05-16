# -*- coding: utf-8 -*-
"""8_puzzle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y_mfTMzBrQvKdBKBQtSzYq7IsszAfLF4
"""

import numpy as np
from heapq import heapify, heappop, heappush
import time

#Default Initial State
Dimension = 3
puzzle =Dimension**2 - 1
heuristic = 3
init_st = np.array([[1, 2, 3],
                   [5, 0, 6],
                   [4, 7, 8]], dtype=int)
#init = init_st
goal_st = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 0]], dtype=int)
# Choice of Algorithms
def evaluate(heuristic, node):
    #Uniform Cost Search
    if heuristic == 1:
        return 0
    #A* with the Misplaced Tile heuristic
    elif heuristic == 2:
      mismatch = np.sum(node != goal_st)  
      return mismatch if mismatch > 0 else 0 
    # A* with the Manhattan Distance heuristic
    elif heuristic == 3:
        dist = 0
        for i in range(1, puzzle + 1):
            pos = np.where(node == i)
            goal_pos = pos_map[i]
            dist += abs(pos[0][0] - goal_pos[0]) + abs(pos[1][0] - goal_pos[1])
        return dist
    else:
        return -1

#Function for checking goal state
def goal_test(node):
    return np.array_equal(node, goal_st)

#Checking for 4 way valid move
def get_valid_moves(state, x, y):
    moves = []
    for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_x, new_y = x + i, y + j
        if (0 <= new_x < state.shape[0]) and (0 <= new_y < state.shape[1]):
            new_state = np.copy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            moves.append(new_state)
    return moves
#Expansion of nodes in the valid direction
def expand(state):
    x, y = np.where(state == 0)
    return get_valid_moves(state, x[0], y[0])

pos_map = dict()
for i in range(1, puzzle+1):
    ind = np.where(goal_st == i)
    x, y = ind[0][0], ind[1][0]
    pos_map[i] = (x, y)

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.g = 0
        self.h = evaluate(heuristic, state)
        if parent:
            self.g = parent.g + 1
    def f(self):
        return self.g + self.h
    def __lt__(self, other):
        return self.f() < other.f()
    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

def a_star():
    nodes_expanded = 0
    queue = [Node(init_st)]
    heapify(queue)
    max_queue_size = 1
    while len(queue) > 0:
        current = heappop(queue)
        nodes_expanded = nodes_expanded + 1
        if goal_test(current.state):
            return current, nodes_expanded, max_queue_size
        children = [Node(ch, parent=current) for ch in expand(current.state)]
        for ch in children:
            if current.parent is None or np.count_nonzero(ch.state == current.parent.state) < puzzle + 1:
                heappush(queue, ch)
        if max_queue_size < len(queue):
            max_queue_size = len(queue)
    return None, nodes_expanded, max_queue_size

if __name__ == '__main__':
    result, nodes_expanded, max_queue_size = None, 0, 0
    print("Choose your input option:\n1 -> Select default option\n2 -> Option for Custom choice")
    choice = int(input())
    if choice == 1:
        start = time.time()
        result, nodes_expanded, max_queue_size = a_star()
        end = time.time()
        print("Time elapsed: ", end - start)
    elif choice == 2:
        
        print("Please input your puzzle, using a zero to represent the blank space.")
        print("Enter the puzzle row by row, ensuring that only valid 8-puzzles from 1 to 8 are entered. Separate each number with a space.")
        print("Enter the first row: ")
        r1 = input()
        print("Enter the second row: ")
        r2 = input()
        print("Enter the third row: ")
        r3 = input()
        init_st[0] = np.array([int(j) for j in r1.split()])
        init_st[1] = np.array([int(j) for j in r2.split()])
        init_st[2] = np.array([int(j) for j in r3.split()])
        print("Choose the heuristic Algorithm:\n1 -> Uniform Cost Search\n2 -> Misplaced Tiles\n3 -> Manhattan Distance")
        heuristic = int(input())
        result, nodes_expanded, max_queue_size = a_star()
    else:
        print("Your choice is invalid")
    if result is not None:
        solution_steps = []
        st = result
        while st is not None:
            solution_steps.append(st)
            st = st.parent
        print("Solution Depth: ", result.g)
        print("Number of Nodes Expanded: ", nodes_expanded)
        print("Max queue size: ", max_queue_size)
        print("The solution steps are as follows:")
        for k in reversed(solution_steps):
            print("The best state to expand with g(n) = ", str(k.g), "and h(n) = ", str(k.h))
            print(k.state)