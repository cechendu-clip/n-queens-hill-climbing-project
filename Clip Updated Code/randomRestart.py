from hillclimbing import hill_climbing, hill_climbing_sideways
from heuristic import validate_n

# Algorithm 3 & 4: Random-Restart Hill-Climbing Without/With Sideways Move
def random_restart_hill_climbing(n: int, sw: bool = False):
    """
    Random-restart hill-climbing: repeatedly run hill-climbing from fresh random states until a goal (h=0) is found.

    [Slide 28: "It conducts a series of hill-climbing searches from randomly generated initial states, until a goal is found
    It is complete with probability approaching 1, because it will eventually generate a goal state as the initial state"]

    [Slide 29: "Random-restart hill climbing overcomes local maxima - trivially complete"]
    [Slide 30: With no sideways moves p~0.14 -> expected ~7 restarts, ~22 steps]
    [Slide 31: With sideways moves p~0.94 -> expected ~1.06 restarts, ~25 steps]

    Args:
        n: board size (number of queens)
        sw: if True, each inner search uses hill_climbing_sideways

    Returns: (restarts, t_steps, final, atts)
        restarts: number of times a new random state was generated after the attempt (total attempts - 1)
        total_steps: cumulative step count across all inner hill-climbing runs
        final: goal state found
        attempts: list of (success, steps, h_seq, states) for every attempt
    """
    validate_n(n)
    
    algo = hill_climbing_sideways if sw else hill_climbing
    total_steps = 0
    restarts = 0 # counts starts beyond first
    attempts = []
    
    while True:
        success, steps, final, h_seq, states = algo(n)
        total_steps += steps
        attempts.append((success, steps, h_seq, states))
        
        if success:
            return restarts, total_steps, final, attempts
        
        # [Slide 28: "if at first you don't succeed, try, try again"]
        restarts += 1

# Trial Runner
def _run_rr_trials(n: int, nt: int, sw: bool):
    """
    Run random-restart hill-climbing nt times and average results
    [Project spec section C: "The average number of random restarts required without/with sideways move" & "The average number of steps required without/with sideways move"]
    """
    validate_n(n)

    if nt <= 0:
        raise ValueError("nt must be a positive integer")
    
    t_rest = 0
    t_steps = 0
    
    for _ in range(nt):
        restarts, steps, _, _ = random_restart_hill_climbing(n, sw)
        t_rest += restarts
        t_steps += steps
    return {
        "trials": nt,
        "avg_restarts": t_rest / nt,
        "avg_steps": t_steps / nt,
    }
