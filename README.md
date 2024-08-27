# Kakuro Solver with Backtracking and Arc-Consistency

## Overview

Kakuro is a logic puzzle that combines elements of crosswords with arithmetic. The goal is to fill a grid with digits (1 through 9) such that the sum of the digits in each block (both horizontally and vertically) matches the given clues. No digit may repeat within any block.

<img width="650" alt="Screenshot 1403-06-06 at 9 11 40 AM" src="https://github.com/user-attachments/assets/009aed23-0d6e-4746-95ac-f5bd958097b6">

This problem can be represented as a Constraint Satisfaction Problem (CSP), where the variables are the white cells in the grid, which must be filled with digits. Constraints include:
- Each digit must be between 1 and 9.
- The sum of the digits in each block must equal the provided clue.
- Digits within each block must be unique.

## Algorithms

### Recursive Backtracking

The `recursive_backtracking` function is designed to solve Kakuro puzzles using both basic and improved backtracking approaches. The function works as follows:

1. **Base Case**: Checks if all variables have been assigned values that satisfy the constraints. If so, it returns the assignment dictionary. If not, it returns `None`.

2. **Recursive Case**: 
   - The function starts by selecting an unassigned variable using `select_unassigned_variable`.
   - It iterates through possible values for this variable based on the domain (which varies depending on whether basic backtracking or 3-AC is used).
   - For each value, it checks consistency with previously assigned values using `is_consistent`.
   - If the value is consistent, it updates the assignment and recursively tries to solve the next variable.
   - If no consistent value is found, it backtracks by removing the last assignment and trying the next possible value.

The search tree in this algorithm can be very large, making optimization essential for efficiency.

### CSP Construction

The `make_CSP` function converts the initial Kakuro grid into a CSP. The process involves:

1. **Variables**: Identifies and categorizes variables into white cells and clue cells (both horizontal and vertical). Each variable is named based on its position and type (e.g., `X1,1` for a white cell at position (1,1), `YD1,1` for a vertical clue, etc.).

2. **Neighbours**: Creates a dictionary mapping each variable to its neighbors. For white cells, neighbors are clue cells that constrain them. For clue cells, neighbors are the white cells they influence.

3. **Domain**: Defines the possible values for each variable. For white cells, the domain is numbers 1 through the minimum constraint value. For clue cells, the domain consists of permutations that sum up to the clue value.

4. **Constraints**: Constructs a dictionary that maps variable pairs to possible values, reflecting the constraints imposed by the clues.

### Arc-Consistency (3-AC)

The `3-AC` function applies the Arc-Consistency algorithm to prune the search space efficiently. It works as follows:

1. **Queue Initialization**: Initializes a queue with all variable pairs (both directions) where variables are neighbors.

2. **Consistency Check**: Iterates over the queue, using `remove_inconsistent_values` to remove values from the domain of one variable based on the domain of its neighboring variable.

3. **Propagation**: Updates the queue with affected variable pairs if the domain of a variable changes.

4. **Termination**: The function returns `True` if the domains are consistent, otherwise `False` if an empty domain is detected, indicating no solution exists.

## Class `KakuroCSP`

The `KakuroCSP` class encapsulates the CSP problem for Kakuro puzzles. It provides methods for handling variables, domains, and constraints:

- **`domain_values(variable)`**: Returns the domain of a given variable.
- **`is_consistent(variable, value, assignment)`**: Checks if assigning a value to a variable is consistent with the current assignment.
- **`remove_inconsistent_values(var1, var2)`**: Removes values from `var1`'s domain that are inconsistent with `var2`'s domain.
- **`select_unassigned_variable(assignment)`**: Selects an unassigned variable from the list of variables.

## Usage

Two scripts are available to test the algorithms:

1. **`kakuro.py`**: Implements basic backtracking for solving Kakuro puzzles.
2. **`kakuro-AC-3.py`**: Implements improved backtracking with 3-AC for solving Kakuro puzzles.

Both scripts allow users to input puzzles, solve them, and measure execution time.

## Results

The following table summarizes the performance of the algorithms on various grid sizes:

| Grid Size | Time (Simple Backtracking) | Time (Backtracking with 3-AC) |
|-----------|-----------------------------|-------------------------------|
| 6x5       | 0.01633                     | 0.00717                       |
| 8x8       | Not feasible in reasonable time | 0.26012                       |
| 10x10     | Not feasible in reasonable time | 1.29222                       |

The results demonstrate that using 3-AC significantly reduces the solving time for larger puzzles compared to basic backtracking.

Feel free to explore the provided scripts and functions to understand the implementation details and improve upon the current algorithms.
