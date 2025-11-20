import copy
import random
from collections import defaultdict

class SudokuBoard:
    def __init__(self, grid):
        # Validate shape & values
        if not isinstance(grid, list) or len(grid) != 9 or any(not isinstance(row, list) or len(row) != 9 for row in grid):
            raise ValueError("Grid must be 9x9 list of lists")
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                if not isinstance(val, int) or not (0 <= val <= 9):
                    raise ValueError("Grid values must be integers 0..9")
        self.grid = copy.deepcopy(grid)
        self.size = 9
        # check initial contradictions
        if not self._initial_valid():
            raise ValueError("Initial grid violates Sudoku rules (duplicate in row/col/box)")

    # ------------------------------
    # Basic rule check
    # ------------------------------
    # Check if placing `num` at (row, col) is valid
    def is_valid(self, row, col, num):
        if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
            return False
        # Row
        for i in range(9):
            if self.grid[row][i] == num:
                return False
        # Column
        for i in range(9):
            if self.grid[i][col] == num:
                return False
        # Box
        sr = 3 * (row // 3)
        sc = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[sr + i][sc + j] == num:
                    return False
        return True

    # ------------------------------
    # Internal: initial validity (no duplicates among givens)
    # ------------------------------
    def _initial_valid(self):
        # check rows, cols, boxes for duplicates ignoring zeros
        for r in range(9):
            seen = set()
            for v in self.grid[r]:
                if v == 0: continue
                if v in seen: return False
                seen.add(v)
        for c in range(9):
            seen = set()
            for r in range(9):
                v = self.grid[r][c]
                if v == 0: continue
                if v in seen: return False
                seen.add(v)
        for br in range(0,9,3):
            for bc in range(0,9,3):
                seen = set()
                for i in range(3):
                    for j in range(3):
                        v = self.grid[br+i][bc+j]
                        if v == 0: continue
                        if v in seen: return False
                        seen.add(v)
        return True

    # ------------------------------
    # find empty cell (MRV optional)
    # ------------------------------
    # Returns (row, col) of first empty cell found, or None if full
    # 從左到右、上到下找第一個為 0 的格子，回傳 (row, col)。
    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return (r, c)
        return None

    # ------------------------------
    # candidates for a cell
    # ------------------------------
    # 找出 (row, col) 可以放的所有合法數字（1–9）。
    def candidates(self, row, col):
        if self.grid[row][col] != 0:
            return []
        cand = []
        for n in range(1,10):
            if self.is_valid(row, col, n):
                cand.append(n)
        return cand

    # ------------------------------
    # Solve (standard backtracking). randomize option for generator.
    # ------------------------------
    # 用標準遞迴回溯法解數獨。
    # 可選擇 randomize=True 讓每次嘗試數字順序隨機（用於生成不同解）。
    def solve(self, randomize=False):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        nums = list(range(1,10))
        if randomize:
            random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve(randomize):
                    return True
                self.grid[row][col] = 0
        return False

    # ------------------------------
    # Solve but collect stats: returns (solved_bool, guesses_made)
    # guesses is incremented when branching at a cell with >1 candidate (i.e. a "guess")
    # Use MRV (choose cell with fewest candidates) for efficiency.
    # ------------------------------
    # 解數獨但同時計算「推測次數（guess 次數）」用於難度評估。
    def solve_with_stats(self):
        # find empty with MRV (min remaining values)
        pos = None
        minlen = 10
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    cand = self.candidates(r,c)
                    if len(cand) < minlen:
                        minlen = len(cand)
                        pos = (r,c)
        if pos is None:
            return True, 0
        r, c = pos
        cand = self.candidates(r,c)
        if len(cand) == 0:
            return False, 0
        total_guesses = 0
        # if branching (more than 1 candidate), this point counts as a guess per branch
        for num in cand:
            self.grid[r][c] = num
            solved, sub_guesses = self.solve_with_stats()
            total_guesses += sub_guesses
            if solved:
                # if we had to branch here, count one guess for the branch we took
                if len(cand) > 1:
                    total_guesses += 1
                return True, total_guesses
            self.grid[r][c] = 0
        return False, total_guesses

    # ------------------------------
    # Count all solutions up to a limit (early exit when count >= limit)
    # Useful for uniqueness checking.
    # ------------------------------
    # 計算解的數量，最多計數到 limit（預設 2），用於檢查唯一解。
    # returns 數量（0, 1, 或 2）。
    def count_solutions(self, limit=2):
        def backtrack(board, count):
            if count[0] >= limit:
                return
            # find empty with MRV
            pos = None
            minlen = 10
            for rr in range(9):
                for cc in range(9):
                    if board[rr][cc] == 0:
                        cand = []
                        for n in range(1,10):
                            ok = True
                            # check row
                            for k in range(9):
                                if board[rr][k] == n:
                                    ok = False; break
                            if not ok: continue
                            # check col
                            for k in range(9):
                                if board[k][cc] == n:
                                    ok = False; break
                            if not ok: continue
                            # check box
                            sr = 3*(rr//3); sc = 3*(cc//3)
                            for i in range(3):
                                for j in range(3):
                                    if board[sr+i][sc+j] == n:
                                        ok = False; break
                                if not ok: break
                            if ok:
                                cand.append(n)
                        if len(cand) < minlen:
                            minlen = len(cand)
                            pos = (rr, cc, cand)
            if pos is None:
                count[0] += 1
                return
            rr, cc, cand = pos
            if len(cand) == 0:
                return
            for n in cand:
                board[rr][cc] = n
                backtrack(board, count)
                board[rr][cc] = 0
                if count[0] >= limit:
                    return

        board_copy = copy.deepcopy(self.grid)
        counter = [0]
        backtrack(board_copy, counter)
        return counter[0]

    # ------------------------------
    # Generator with uniqueness guarantee: remove cells one by one,
    # and only keep removal if solution-count remains 1.
    # ------------------------------
    # 生成一個 保證唯一解 的數獨題。
    def generate_unique(self, difficulty):
        base = SudokuBoard([[0]*9 for _ in range(9)])
        base.solve(randomize=True)
        puzzle = SudokuBoard(base.grid)
        # create list of cell indices and shuffle to attempt removals in random order
        cells = [(r,c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        removed = 0
        attempts = 0
        # Attempt removals until we've removed `difficulty` cells or we ran out of cells
        for (r,c) in cells:
            if removed >= difficulty:
                break
            # try remove
            if puzzle.grid[r][c] == 0:
                continue
            saved = puzzle.grid[r][c]
            puzzle.grid[r][c] = 0
            sb = SudokuBoard(puzzle.grid)  # validated board
            cnt = sb.count_solutions(limit=2)
            if cnt == 1:
                removed += 1
            else:
                # revert
                puzzle.grid[r][c] = saved
            attempts += 1
        return puzzle, base

    # ------------------------------
    # Difficulty rating:
    # - Try logical solving (naked & hidden singles). If solved => Easy
    # - Else run solve_with_stats to get guesses:
    #     guesses == 0 => Easy (shouldn't happen)
    #     1..9 => Medium
    #     >=10 => Hard
    # ------------------------------
    # 給目前盤面評估難度（Easy / Medium / Hard）。
    # def difficulty_rating(self):
    #     # working copy
    #     working = SudokuBoard(self.grid)
    #     progress = True
    #     while progress:
    #         progress = False
    #         # naked singles: 顯性單一：該格唯一可能
    #         for r in range(9):
    #             for c in range(9):
    #                 if working.grid[r][c] == 0:
    #                     cand = working.candidates(r,c)
    #                     if len(cand) == 1:
    #                         working.grid[r][c] = cand[0]
    #                         progress = True
    #         # hidden singles: 隱性單一：該數字在該列/行/宮格唯一可能位置
    #         # rows
    #         for r in range(9):
    #             counts = defaultdict(list)
    #             for c in range(9):
    #                 if working.grid[r][c] == 0:
    #                     for n in working.candidates(r,c):
    #                         counts[n].append((r,c))
    #             for n, poslist in counts.items():
    #                 if len(poslist) == 1:
    #                     rr,cc = poslist[0]
    #                     working.grid[rr][cc] = n
    #                     progress = True
    #         # cols
    #         for c in range(9):
    #             counts = defaultdict(list)
    #             for r in range(9):
    #                 if working.grid[r][c] == 0:
    #                     for n in working.candidates(r,c):
    #                         counts[n].append((r,c))
    #             for n, poslist in counts.items():
    #                 if len(poslist) == 1:
    #                     rr,cc = poslist[0]
    #                     working.grid[rr][cc] = n
    #                     progress = True
    #         # boxes
    #         for br in range(0,9,3):
    #             for bc in range(0,9,3):
    #                 counts = defaultdict(list)
    #                 for i in range(3):
    #                     for j in range(3):
    #                         r = br+i; c = bc+j
    #                         if working.grid[r][c] == 0:
    #                             for n in working.candidates(r,c):
    #                                 counts[n].append((r,c))
    #                 for n, poslist in counts.items():
    #                     if len(poslist) == 1:
    #                         rr,cc = poslist[0]
    #                         working.grid[rr][cc] = n
    #                         progress = True
    #     # if solved by logical techniques:
    #     if all(all(cell != 0 for cell in row) for row in working.grid):
    #         return "Easy"
    #     # otherwise use solve_with_stats
    #     copy_for_stats = SudokuBoard(self.grid)
    #     solved, guesses = copy_for_stats.solve_with_stats()
    #     if not solved:
    #         return "Unsolvable"
    #     if guesses == 0:
    #         return "Easy"
    #     if guesses < 10:
    #         return "Medium"
    #     return "Hard"

# ------------------------------
# Convenience top-level generate functions
# ------------------------------
# 簡易版生成題目（不保證唯一解）。
def generate(difficulty):
    # simple generator without uniqueness guarantee
    empty_grid = [[0]*9 for _ in range(9)]
    solution_board = SudokuBoard(empty_grid)
    solution_board.solve(randomize=True)
    puzzle_board = SudokuBoard(solution_board.grid)
    holes = difficulty
    cells = [(r,c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    idx = 0
    while holes > 0 and idx < len(cells):
        r,c = cells[idx]
        idx += 1
        if puzzle_board.grid[r][c] != 0:
            puzzle_board.grid[r][c] = 0
            holes -= 1
    return puzzle_board, solution_board

def generate_unique(difficulty):
    base = SudokuBoard([[0]*9 for _ in range(9)])
    base.solve(randomize=True)
    # use SudokuBoard.generate_unique via instance
    return base.generate_unique(difficulty)
