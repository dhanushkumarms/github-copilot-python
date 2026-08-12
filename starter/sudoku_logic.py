import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board, clues):
    """Remove cells from a filled board to create a puzzle.

    Cells are removed one at a time, but only kept empty if doing so
    still leaves the puzzle with exactly one unique solution. If removing
    a cell would create multiple solutions, the number is restored and a
    different cell is tried instead. This guarantees every generated
    puzzle has a single, unique solution.
    """
    # Import here to avoid a circular import at module load time,
    # since solver.py imports from sudoku_logic.py
    from solver import count_solutions

    attempts = SIZE * SIZE - clues
    # Cap total tries to avoid an infinite loop if too few cells are
    # safely removable for the requested number of clues.
    max_tries = SIZE * SIZE * 10
    tries = 0

    while attempts > 0 and tries < max_tries:
        tries += 1
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)

        if board[row][col] == EMPTY:
            continue

        removed_value = board[row][col]
        board[row][col] = EMPTY

        # Check uniqueness on a copy so we don't disturb the real board
        # while counting solutions.
        board_copy = deep_copy(board)
        if count_solutions(board_copy, limit=2) != 1:
            # Removing this cell created multiple solutions; put it back.
            board[row][col] = removed_value
        else:
            attempts -= 1

def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
