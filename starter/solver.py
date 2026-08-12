"""Solver utilities for validating Sudoku puzzles.

This module is used to check how many solutions a given board has,
which lets us confirm that generated puzzles have exactly one unique
solution before presenting them to the player.
"""

from sudoku_logic import SIZE, EMPTY, is_safe


def count_solutions(board, limit=2):
    """Count how many valid solutions a Sudoku board has.

    Uses backtracking to search for solutions, but stops early once
    `limit` solutions have been found. This keeps the check fast,
    since we only care whether the puzzle has exactly one solution
    (we don't need the exact count if there are many).

    Args:
        board: A 9x9 list of lists representing the current board state.
        limit: Stop searching once this many solutions have been found.

    Returns:
        The number of solutions found (capped at `limit`).
    """
    count = [0]  # Use a list so the nested function can modify it (closure workaround)

    def backtrack():
        # Stop early if we've already hit the limit
        if count[0] >= limit:
            return

        # Find the next empty cell
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    for num in range(1, SIZE + 1):
                        if is_safe(board, row, col, num):
                            board[row][col] = num
                            backtrack()
                            board[row][col] = EMPTY
                            if count[0] >= limit:
                                return
                    return  # No valid number fits here; backtrack further

        # No empty cells left means we found a complete solution
        count[0] += 1

    backtrack()
    return count[0]