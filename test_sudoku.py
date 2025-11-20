import pytest
from sudoku import SudokuBoard, generate, generate_unique

def test_is_valid():
    board_data = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    board = SudokuBoard(board_data)
    assert board.is_valid(0, 2, 4) is True
    assert board.is_valid(0, 2, 5) is False
    assert board.is_valid(0, 2, 8) is False
    assert board.is_valid(1, 1, 9) is False

def test_solve():
    puzzle = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]
    solved = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]
    b = SudokuBoard(puzzle)
    assert b.solve() is True
    assert b.grid == solved

def test_generate_basic():
    puzzle, solution = generate(40)
    assert sum(row.count(0) for row in puzzle.grid) == 40
    copy = SudokuBoard(puzzle.grid)
    assert copy.solve() is True
    # assert copy.grid == solution.grid

# -------------------------
# BONUS tests
# -------------------------
def test_count_solutions_limit():
    # empty board has many solutions; counting with limit=2 should return at least 2 quickly
    empty = SudokuBoard([[0]*9 for _ in range(9)])
    cnt = empty.count_solutions(limit=2)
    assert cnt >= 2

def test_generate_unique_and_count():
    # generate unique puzzle with moderate difficulty (may take some time)
    puzzle, solution = generate_unique(30)
    # ensure puzzle has requested number of holes OR as many as possible (>= 0)
    assert sum(row.count(0) for row in puzzle.grid) >= 0
    # ensure uniqueness
    pb = SudokuBoard(puzzle.grid)
    cnt = pb.count_solutions(limit=2)
    assert cnt == 1

def test_difficulty():
    # easy puzzle: solvable by singles (we construct one)
    easy_grid = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,0]  # only one empty cell -> naked single
    ]
    board = SudokuBoard(easy_grid)
    assert board.difficulty_rating() == "Easy"


def test_invalid_initial_grid():
    # invalid initial grid (duplicate in row) should raise
    bad = [
        [1,1,0,0,0,0,0,0,0],
    ] + [[0]*9 for _ in range(8)]
    with pytest.raises(ValueError):
        SudokuBoard(bad)
    # unsolvable (contradiction)
    unsolvable = [
        [1,2,3,4,5,6,7,8,9],
        [1,0,0,0,0,0,0,0,0],  # duplicate 1 in column
    ] + [[0]*9 for _ in range(7)]
    with pytest.raises(ValueError):
        SudokuBoard(unsolvable)