import os
from heuristic import random_state
from hillclimbing import hill_climbing, hill_climbing_sideways, _run_trials
from randomRestart import random_restart_hill_climbing, _run_rr_trials

# board rendering
def board_to_string(state, indent="  "):
    n = len(state)
    b = indent + "+" + "-" * (n * 2 + 1) + "+"
    out = [b]
    for row in range(n):
        c = " ".join("Q" if state[col] == row else "." for col in range(n))
        out.append(f"{indent}| {c} |")
    out.append(b)
    return "\n".join(out)

# terminal printing
def _print_table(rows, headers):
    widths = [max(len(h), max(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    fmt = "| " + " | ".join(f"{{:<{w}}}" for w in widths) + " |"
    print(sep)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*row))
    print(sep)

def print_hill_climbing_report(n, sw=False):
    lbl = "Hill-Climbing (Sideways)" if sw else "Hill-Climbing (No Sideways)"
    print(f"\n{lbl} - {n}-Queens\n")
    rows = []
    for t in [50, 100, 200, 500, 1000, 1500]:
        s = _run_trials(n, t, sw)
        avg_s = f"{s['avg_steps_success']:.2f}" if s['successes'] > 0 else "N/A"
        avg_f = f"{s['avg_steps_failure']:.2f}" if s['failures'] > 0 else "N/A"
        rows.append((str(t), f"{s['success_rate']:.1f}%", f"{s['failure_rate']:.1f}%", avg_s, avg_f))
    _print_table(rows, ["Trials", "Success%", "Failure%", "Avg Steps (S)", "Avg Steps (F)"])
    algo = hill_climbing_sideways if sw else hill_climbing
    print(f"\n4 Random Runs ({lbl}):\n")
    run_rows = []
    for i in range(4):
        init = random_state(n)
        ok, st, _, hs, _ = algo(n, init)
        outcome = "SUCCESS" if ok else "FAILURE"
        run_rows.append((f"Run {i + 1}", outcome, f"{st} step(s)", str(init), f"h: {hs[0]} -> {hs[-1]}"))
    _print_table(run_rows, ["", "Result", "Steps", "Initial State", "h change"])

def print_random_restart_report(n, runs=100):
    print(f"\nRandom-Restart - {n}-Queens (averaged over {runs} runs)\n")
    s_no = _run_rr_trials(n, runs, False)
    s_sw = _run_rr_trials(n, runs, True)
    rows = [
        ("Random-Restart (No Sideways)", f"{s_no['avg_restarts']:.2f}", f"{s_no['avg_steps']:.2f}"),
        ("Random-Restart (Sideways)",    f"{s_sw['avg_restarts']:.2f}", f"{s_sw['avg_steps']:.2f}"),
    ]
    _print_table(rows, ["Variant", "Avg Restarts", "Avg Steps"])

# export helpers
def _write_trace(out, rn, ok, st, hs, ss, sw):
    out.append(f"### Run {rn} - {'SUCCESS' if ok else 'FAILURE'} ({st} step(s))")
    out.append("")
    last = len(ss) - 1
    for i, (state, h) in enumerate(zip(ss, hs)):
        if i == 0:
            lbl = "step 0 (initial state)"
        elif i == last:
            lbl = f"step {last} (solution)" if ok else f"step {last} (stuck at h={h})"
        else:
            lbl = f"step {i}"
        out.append(f"**{lbl}:** `{state}`  (h={h})")
        out.append("```")
        out.append(board_to_string(state, indent=""))
        out.append("```")
    out.append("")

# export: hill-climbing (sections A and B)
def export_hill_climbing_report(n, fp, sw=False):
    lbl = "Hill-Climbing (Sideways)" if sw else "Hill-Climbing (No Sideways)"
    out = []
    out.append(f"# {lbl} - {n}-Queens\n")
    out.append("| Trials | Success% | Failure% | Avg Steps (S) | Avg Steps (F) |")
    out.append("|---:|---:|---:|---:|---:|")
    for t in [50, 100, 200, 500, 1000, 1500]:
        s = _run_trials(n, t, sw)
        avg_s = f"{s['avg_steps_success']:.2f}" if s['successes'] > 0 else "N/A"
        avg_f = f"{s['avg_steps_failure']:.2f}" if s['failures'] > 0 else "N/A"
        out.append(f"| {t} | {s['success_rate']:.1f} | {s['failure_rate']:.1f} | {avg_s} | {avg_f} |")
    out.append("")
    out.append("## 4 Random Runs with Board Simulation Steps:\n")
    algo = hill_climbing_sideways if sw else hill_climbing
    for i in range(4):
        init = random_state(n)
        ok, st, _, hs, ss = algo(n, init)
        _write_trace(out, i + 1, ok, st, hs, ss, sw)
    with open(fp, "w") as f:
        f.write("\n".join(out))

# export: random-restart (section C)
def export_random_restart_report(n, fp, runs=100):
    out = []
    out.append(f"# Random-Restart - {n}-Queens\n")
    out.append("| Variant | Avg Restarts | Avg Steps |")
    out.append("|---|---:|---:|")
    s_no = _run_rr_trials(n, runs, False)
    s_sw = _run_rr_trials(n, runs, True)
    out.append(f"| Random-Restart (No Sideways) | {s_no['avg_restarts']:.2f} | {s_no['avg_steps']:.2f} |")
    out.append(f"| Random-Restart (Sideways) | {s_sw['avg_restarts']:.2f} | {s_sw['avg_steps']:.2f} |\n")
    for sw in (False, True):
        v = "Random-Restart (Sideways)" if sw else "Random-Restart (No Sideways)"
        out.append(f"## Example Trace - {v}\n")
        r, ts, _, atts = random_restart_hill_climbing(n, sw)
        for idx, (ok, st, hs, ss) in enumerate(atts):
            _write_trace(out, idx + 1, ok, st, hs, ss, sw)
        out.append(f"total attempts: {r + 1}  |  total steps: {ts}\n")
    with open(fp, "w") as f:
        f.write("\n".join(out))
