import random
from typing import List, Tuple

State = List[int]

def validate_n(n: int) -> None:
    """Validate board size for the N-Queens problem."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be a postive integer")

"""
State Representation:
[Slide 14: "Local search algorithms typically use a complete-state formulation, where each state has 8 queens on the board, one per column"]
state = list of length n, where state[col] = row index of the queen in that column
All n queens are always on the board (complete-state); neighbors are formed by moving one queen to a different row within the same column
[Slide 15: "# of successors of a state = 8 * 7 = 56 successors" -> generalized to n*(n-1)]
"""

def compute_heuristic(state: State)-> int: 
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

def random_state(n: int) -> State:
    # generate random complete-state: one queen per column in random row
    validate_n(n) #checks n is integer and positive 
    return [random.randint(0, n - 1) for _ in range(n)]

def get_best_neighbors(state: State) -> Tuple[int, List[State]]:
    """
    [Slide 10 pseudocode: "neighbor <- a highest-valued successor of current"; since we minimize h, we pick the neighbor with the lowest h.]
    Evaluate all n*(n-1) neighbors (move each queen within its column) and return the minimum heuristic value found together with all neighbor states that achieve that minimum.

    Returns: (best_h, best_nbrs)
        best_h: lowest h value among all neighbors
        best_nbrs: list of neighbor states achieving best_h
    """
    n = len(state)
    best_h = None
    best_nbrs: List[State] = []
    
    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row == original_row:
                continue # skip current position
            
            neighbor = state.copy()
            neighbor[col] = row
            h = compute_heuristic(neighbor)
            
            if best_h is None or h < best_h:
                best_h = h
                best_nbrs = [neighbor]
            elif h == best_h:
                best_nbrs.append(neighbor)
                
    # for n=1 there are no neighbors; treat the current state as already solved.            
    if best_h is None:
        return compute_heuristic(state), [state.copy()]
    
    return best_h, best_nbrs
