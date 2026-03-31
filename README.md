# N-Queens Hill-Climbing Project

This project implements and analyzes several hill-climbing approaches for solving the **N-Queens problem**, with experimental evaluation focused on the **8-Queens problem**.

## Project Overview

The N-Queens problem asks how to place **N queens** on an **N × N chessboard** so that no two queens attack each other. This means that no two queens can share the same row, column, or diagonal.

This project explores the performance of the following local search methods:

- Standard hill-climbing
- Hill-climbing with sideways moves
- Random-restart hill-climbing without sideways moves
- Random-restart hill-climbing with sideways moves

The program allows the user to enter any value of `n`, but the main experimental analysis in this project is based on the **8-Queens problem**.

---

## Files in the Repository

### `heuristic.py`
Contains the core utility functions for the N-Queens problem, including:
- Board validation
- Random state generation
- Heuristic computation
- Best-neighbor generation

### `hillclimbing.py`
Implements:
- Standard hill-climbing
- Hill-climbing with sideways moves
- Trial-running functions for collecting statistics

### `randomRestart.py`
Implements:
- Random-restart hill-climbing
- Trial-running functions for average restarts and average steps

### `printAlgResult.py`
Handles:
- Output formatting
- Terminal report printing
- Markdown report generation
- Search-sequence display

### `main.py`
The main entry point of the program. It:
- Prompts the user for `n`
- Runs the algorithms
- Prints results
- Exports markdown reports

---

## Algorithms Implemented

### 1. Standard Hill-Climbing
Starts from a random initial state and repeatedly moves to the neighbor with the lowest heuristic value, but only if it is strictly better than the current state.

### 2. Hill-Climbing with Sideways Moves
Similar to standard hill-climbing, but also allows moves to neighbors with the same heuristic value. This helps the search move across plateaus.

### 3. Random-Restart Hill-Climbing
Repeats hill-climbing from new random initial states until a solution is found.

### 4. Random-Restart Hill-Climbing with Sideways Moves
Combines random restarts with sideways moves for stronger performance and higher reliability.

---

## Heuristic Function

The heuristic function used in this project is the **number of attacking pairs of queens**.

A heuristic value of:
- `0` means a valid solution has been found
- A higher value means more conflicts remain

---

## Experimental Focus

The required experiments were performed on the **8-Queens problem** using multiple trial sizes:

- 50
- 100
- 200
- 500
- 1000
- 1500

The program reports:
- Success rate
- Failure rate
- Average steps for successful runs
- Average steps for failed runs

For random-restart hill-climbing, the report also includes:
- Average random restarts
- Average total steps

---

## How to Run

Make sure you have Python 3 installed.

Run the project with:

```bash
python main.py
