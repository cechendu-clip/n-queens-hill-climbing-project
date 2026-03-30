import os
from typing import List

from heuristic import random_state
from hillclimbing import hill_climbing, hill_climbing_sideways, _run_trials
from randomRestart import random_restart_hill_climbing, _run_rr_trials

# board rendering
def board_to_string(state, indent="  "):
    n = len(state)
    border = indent + "+" + "-" * (n * 2 + 1) + "+"
    lines = [border]
    for row in range(n):
        content = " ".join("Q" if state[col] == row else "." for col in range(n))
        lines.append(f"{indent}| {content} |")
    lines.append(border)
    return "\n".join(lines)

# terminal printing
def _print_table(rows: List[List[str]], headers: List[str]) -> None:
    widths = []
    for col_index, header in enumerate(headers):
        max_row_width = max(len(str(row[col_index])) for row in rows) if rows else 0
        widths.append(max(len(header), max_row_width))

    sep = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    fmt = "| " + " | ".join(f"{{:<{width}}}" for width in widths) + " |"

    print(sep)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*row))
    print(sep)


# sections A and B
def print_hill_climbing_report(n: int, sw: bool = False) -> None:
    label = "Hill-climbing with sideways moves" if sw else "Hill-climbing"
    print(f"\nReport: {label} for {n}-Queens\n")

    rows: List[List[str]] = []
    for t in [50, 100, 200, 500, 1000, 1500]:
        s = _run_trials(n, t, sw)
        avg_s = f"{s['avg_steps_success']:.2f}" if s["successes"] > 0 else "N/A"
        avg_f = f"{s['avg_steps_failure']:.2f}" if s["failures"] > 0 else "N/A"
        rows.append([
            str(t),
            f"{s['success_rate']:.2f}%",
            f"{s['failure_rate']:.2f}%",
            avg_s,
            avg_f,
        ])

    _print_table(
        rows,
        ["Trials", "Success Rate", "Failure Rate", "Avg Steps (Success)", "Avg Steps (Failure)"],
    )

    print("\nSearch sequences from four random initial configurations:\n")
    trace_rows: List[List[str]] = []
    algo = hill_climbing_sideways if sw else hill_climbing

    for _ in range(4):
        init = random_state(n)
        ok, steps, final_state, hs, _ = algo(n, init)
        trace_rows.append([
            str(init),
            str(hs[0]),
            str(hs[-1]),
            str(steps),
            "SUCCESS" if ok else "FAILURE",
            "goal" if ok else "local_minimum_or_plateau",
        ])

    _print_table(
        trace_rows,
        ["Initial State", "Initial h", "Final h", "Steps", "Result", "Stopped Because"],
    )


# section C
def print_random_restart_report(n: int, runs: int = 100) -> None:
    print(f"\nReport: Random-restart hill-climbing for {n}-Queens\n")

    s_no = _run_rr_trials(n, runs, False)
    s_sw = _run_rr_trials(n, runs, True)

    rows = [
        ["Without sideways move", f"{s_no['avg_restarts']:.2f}", f"{s_no['avg_steps']:.2f}"],
        ["With sideways move", f"{s_sw['avg_restarts']:.2f}", f"{s_sw['avg_steps']:.2f}"],
    ]
    _print_table(rows, ["Variant", "Avg Random Restarts", "Avg Steps"])


# export helpers
def _write_trace(out: List[str], rn: int, ok: bool, st: int, hs, ss) -> None:
    out.append(f"### Search Sequence {rn}")
    out.append("")
    out.append(f"- Result: {'SUCCESS' if ok else 'FAILURE'}")
    out.append(f"- Steps: {st}")
    out.append(f"- Stopped Because: {'goal' if ok else 'local_minimum_or_plateau'}")
    out.append("")

    for step_number, (state, h_value) in enumerate(zip(ss, hs)):
        out.append(f"**Step {step_number}** — state `{state}` with `h = {h_value}`")
        out.append("```")
        out.append(board_to_string(state, indent=""))
        out.append("```")
    out.append("")


# export: hill-climbing (sections A and B)
def export_hill_climbing_report(n: int, fp: str, sw: bool = False) -> None:
    label = "Hill-climbing with sideways moves" if sw else "Hill-climbing"
    out: List[str] = [
        f"# {label} Report for {n}-Queens",
        "",
        "## Success and failure statistics",
        "",
        "| Trials | Success Rate | Failure Rate | Avg Steps (Success) | Avg Steps (Failure) |",
        "|---:|---:|---:|---:|---:|",
    ]

    for t in [50, 100, 200, 500, 1000, 1500]:
        s = _run_trials(n, t, sw)
        avg_s = f"{s['avg_steps_success']:.2f}" if s["successes"] > 0 else "N/A"
        avg_f = f"{s['avg_steps_failure']:.2f}" if s["failures"] > 0 else "N/A"
        out.append(
            f"| {t} | {s['success_rate']:.2f}% | {s['failure_rate']:.2f}% | {avg_s} | {avg_f} |"
        )

    out.extend(["", "## Search sequences from four random initial configurations", ""])

    algo = hill_climbing_sideways if sw else hill_climbing
    for index in range(1, 5):
        init = random_state(n)
        ok, st, final_state, hs, ss = algo(n, init)
        _write_trace(out, index, ok, st, hs, ss)

    with open(fp, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out))


# export: random-restart (section C)
def export_random_restart_report(n: int, fp: str, runs: int = 100) -> None:
    out: List[str] = [
        f"# Random-Restart Report for {n}-Queens",
        "",
        f"Average results computed over {runs} independent runs.",
        "",
        "| Variant | Avg Random Restarts | Avg Steps |",
        "|---|---:|---:|",
    ]

    s_no = _run_rr_trials(n, runs, False)
    s_sw = _run_rr_trials(n, runs, True)
    out.append(f"| Without sideways move | {s_no['avg_restarts']:.2f} | {s_no['avg_steps']:.2f} |")
    out.append(f"| With sideways move | {s_sw['avg_restarts']:.2f} | {s_sw['avg_steps']:.2f} |")

    out.extend(["", "## Example random-restart trace without sideways moves", ""])

    restarts_no, total_steps_no, final_no, attempts_no = random_restart_hill_climbing(n, False)
    for index, attempt in enumerate(attempts_no, start=1):
        ok, st, hs, ss = attempt
        _write_trace(out, index, ok, st, hs, ss)
    out.append(f"Total restarts: {restarts_no}")
    out.append(f"Total steps: {total_steps_no}")

    out.extend(["", "## Example random-restart trace with sideways moves", ""])

    restarts_yes, total_steps_yes, final_yes, attempts_yes = random_restart_hill_climbing(n, True)
    for index, attempt in enumerate(attempts_yes, start=1):
        ok, st, hs, ss = attempt
        _write_trace(out, index, ok, st, hs, ss)
    out.append(f"Total restarts: {restarts_yes}")
    out.append(f"Total steps: {total_steps_yes}")

    with open(fp, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out))


# optional helper
def export_all_reports(output_dir: str, n: int) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    files = [
        os.path.join(output_dir, f"{n}queens_hill_climbing.md"),
        os.path.join(output_dir, f"{n}queens_hill_climbing_sideways.md"),
        os.path.join(output_dir, f"{n}queens_random_restart.md"),
    ]
    export_hill_climbing_report(n, files[0], sw=False)
    export_hill_climbing_report(n, files[1], sw=True)
    export_random_restart_report(n, files[2])
    return files
