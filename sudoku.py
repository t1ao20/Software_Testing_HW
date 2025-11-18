import copy
import numbers
import random

class SudokuBoard:
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.size = 9

    def is_valid(self, row, col, num):
        # row check
        for i in range(9):
            if self.grid[row][i] == num:
                return False

        # col check
        for i in range(9):
            if self.grid[i][col] == num:
                return False

        # box check
        start_r = 3 * (row // 3)
        start_c = 3 * (col // 3)

        for i in range(3):
            for j in range(3):
                if self.grid[start_r + i][start_c + j] == num:
                    return False

        return True

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def solve(self, randomize=False):
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty

        nums = list(range(1, 10))

        if randomize:
            random.shuffle(nums)
            
        for num in nums:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num

                if self.solve(randomize):
                    return True

                self.grid[row][col] = 0  # backtrack

        return False

def generate(difficulty):
    empty_grid = [[0]*9 for _ in range(9)]
    solution = SudokuBoard(empty_grid)
    solution.solve(randomize=True)

    puzzle = SudokuBoard(solution.grid)

    holes = difficulty
    while holes > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if puzzle.grid[r][c] != 0:
            puzzle.grid[r][c] = 0
            holes -= 1

    return puzzle, solution
