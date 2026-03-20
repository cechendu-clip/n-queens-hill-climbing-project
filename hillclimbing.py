import random
from heuristic import compute_heuristic, random_state, get_best_neighbor

# Sideways-Move Limit:
# [Slide 23: "put a limit on the number of consecutive sideways moves allowed"]
# [Slide 24: "For example, limit of 100 consecutive sideways moves in the 8-queens problem"]
SIDEWAYS_LIMIT = 100 # global limit

# Algorithm 1: Hill-climbing (no sideways moves)
def hill_climbing(n, init=None):
    """
    Standard stochastic hill-climbing search

    [Slide 10 pseudocode:
    function HILL-CLIMBING(problem) returns a state that is a local maximum
        current <- MAKE-NODE(INITIAL-STATE[problem])
        loop do
            neighbor <- a highest-valued successor of current
            if VALUE[neighbor] <= VALUE[current] then return STATE[current]
            current <- neighbor
        end]

    [Slide 12: "Terminates when it reaches a 'peak' where no neighbor has a higher value"]
    [Slide 22: gets stuck 86% of the time; succeeds ~4 steps avg, fails ~3 steps avg]
    Since we *minimize* h (conflicts), "highest value" becomes "lowest h"; the algorithm stops (gets stuck) when no neighbor has strictly lower h

    Args:
        n: board size (number of queens)
        init: optional starting state; generated randomly if None

    Returns: (success, steps, final, h_seq, states)
        success: True if h=0 was reached
        steps: number of moves taken
        final: board configuration at termination
        h_seq: list of h values recorded at the start and after each move
        states: list of board states parallel to h_seq
    """
    current = init[:] if init is not None else random_state(n)
    h = compute_heuristic(current)
    steps = 0
    h_seq = [h]
    states = [current[:]]

    while True:
        if h == 0: # goal state
            return True, steps, current, h_seq, states

        bh, nbrs = get_best_neighbor(current)

        # [Slide 10: "if VALUE[neighbor] <= VALUE[current] then return STATE[current]"]; stop if best neighbor not strictly better
        if bh >= h:
            return False, steps, current, h_seq, states

        # break ties randomly among equally-best neighbors
        current = random.choice(nbrs)
        h = bh
        steps += 1
        h_seq.append(h)
        states.append(current[:])

# Algorithm 2: Hill-Climbing with Sideways Moves
def hill_climbing_sideways(n, init=None):
    """
    Hill-climbing search that permits sideways moves on plateaus, capped at SIDEWAYS_LIMIT to prevent infinite loops
    [Slide 23: "allow a sideways move in the hope that the plateau is really a shoulder... an infinite loop will occur whenever the algorithm reaches a flat local maximum that is not a shoulder"]
    [Slide 24: limit of 100 consecutive sideways moves raises success rate from 14% to 94%; averages ~21 steps on success, ~64 steps on failure]

    Args:
        n: board size
        init: starting state; generated randomly (if None)

    Returns:
        Same as hill_climbing()
    """
    current = init[:] if init is not None else random_state(n)
    h = compute_heuristic(current)
    steps = 0
    sw_cnt = 0
    h_seq = [h]
    states = [current[:]]

    while True:
        if h == 0:
            return True, steps, current, h_seq, states

        bh, nbrs = get_best_neighbor(current)

        if bh < h:
            # reset consecutive sideways count
            sw_cnt = 0
        elif bh == h:
            # sideways move, check limit
            if sw_cnt >= SIDEWAYS_LIMIT:
                return False, steps, current, h_seq, states
            sw_cnt += 1
        else:
            # all neighbors worse, genuine local minimum
            return False, steps, current, h_seq, states

        current = random.choice(nbrs)
        h = bh
        steps += 1
        h_seq.append(h)
        states.append(current[:])

# Trial Runner
def _run_trials(n, nt, sw):
    """
    Run hill-climbing variants nt times and collect statistics.
    [Project spec: "Run several times, i.e. 50, 100, 200, 500, 1000 to 1500, and report success and failure rates; average number of steps when it succeeds; when it fails"]

    Returns a dict with aggregated statistics.
    """
    algo = hill_climbing_sideways if sw else hill_climbing
    s_steps = []
    f_steps = []

    for _ in range(nt):
        success, steps, _, _, _ = algo(n)
        if success: s_steps.append(steps)
        else: f_steps.append(steps)

    succ = len(s_steps)
    fail = len(f_steps)
    return {
        "trials": nt,
        "successes": succ,
        "failures": fail,
        "success_rate": succ / nt * 100,
        "failure_rate": fail / nt * 100,
        "avg_steps_success": sum(s_steps) / succ if succ else 0.0,
        "avg_steps_failure": sum(f_steps) / fail if fail else 0.0,
    }