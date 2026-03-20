import random

"""
State Representation:
[Slide 14: "Local search algorithms typically use a complete-state formulation, where each state has 8 queens on the board, one per column"]
state = list of length n, where state[col] = row index of the queen in that column
All n queens are always on the board (complete-state); neighbors are formed by moving one queen to a different row within the same column
[Slide 15: "# of successors of a state = 8 * 7 = 56 successors" -> generalized to n*(n-1)]
"""

def compute_heuristic(state):
    """
    [Slide 16: "The heuristic cost function h is the number of pairs of queens that are attacking each other, either directly or indirectly"]
    Return h = number of pairs of queens that are attacking each other
    h = 0 means no conflicts or goal state (solution found)
    """
    n = len(state)
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]: # same row
                h += 1
            if abs(state[i] - state[j]) == abs(i - j): # same diagonal
                h += 1
    return h

def random_state(n):
    # generate random complete-state: one queen per column in random row
    return [random.randint(0, n - 1) for _ in range(n)]

def get_best_neighbor(state):
    """
    [Slide 10 pseudocode: "neighbor <- a highest-valued successor of current"; since we minimize h, we pick the neighbor with the lowest h.]
    Evaluate all n*(n-1) neighbors (move each queen within its column) and return the minimum heuristic value found together with all neighbor states that achieve that minimum.

    Returns: (best_h, best_neighbors)
        best_h: lowest h value among all neighbors
        best_neighbors: list of neighbor states achieving best_h
    """
    n = len(state)
    bh = None
    nbrs = []
    for col in range(n):
        orig = state[col]
        for row in range(n):
            if row == orig:
                continue # skip current position
            neighbor = state[:]
            neighbor[col] = row
            h = compute_heuristic(neighbor)
            if bh is None or h < bh:
                bh = h
                nbrs = [neighbor]
            elif h == bh:
                nbrs.append(neighbor)
    return bh, nbrs