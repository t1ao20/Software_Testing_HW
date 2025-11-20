from sudoku import SudokuBoard, generate, generate_unique
import sys

def print_board(board):
    print("\n   0 1 2   3 4 5   6 7 8")
    print("  -------------------------")
    for r in range(9):
        row_str = f"{r}| "
        for c in range(9):
            val = board.grid[r][c]
            if val == 0:
                row_str += ". "
            else:
                row_str += str(val) + " "
            if (c + 1) % 3 == 0:
                row_str += "| "
        print(row_str)
        if (r + 1) % 3 == 0:
            print("  -------------------------")
    print()


def start_game():
    print("==== Sudoku Game ====\n")
    print("Select difficulty:")
    print("1. Easy (30 holes)")
    print("2. Medium (40 holes)")
    print("3. Hard (50 holes)")
    print("4. Unique (30 holes, guaranteed unique solution)\n")

    choice = input("Choose 1–4: ").strip()

    if choice == "1":
        holes = 30
        puzzle, solution = generate(holes)
    elif choice == "2":
        holes = 40
        puzzle, solution = generate(40)
    elif choice == "3":
        holes = 50
        puzzle, solution = generate(50)
    elif choice == "4":
        holes = 30
        print("Generating unique puzzle... might take ~5 seconds...")
        puzzle, solution = generate_unique(holes)
    else:
        print("Invalid choice")
        return

    board = SudokuBoard(puzzle.grid)

    print("\n=== Your Sudoku Puzzle ===")
    print_board(board)

    while True:
        cmd = input("Enter command (help for options): ").strip().lower()

        if cmd == "help":
            print("""
Commands:
  set r c n   - Put number n at row r, col c
  hint r c    - Show candidates for cell
  show        - Show the board
  solve       - Auto solve
  diff        - Show difficulty rating
  quit        - Exit game
""")

        elif cmd.startswith("set"):
            try:
                _, r, c, n = cmd.split()
                r = int(r); c = int(c); n = int(n)
                if not (0 <= r < 9 and 0 <= c < 9 and 1 <= n <= 9):
                    print("Invalid input (range error)")
                    continue
                if puzzle.grid[r][c] != 0:
                    print("You cannot change a given clue.")
                    continue
                if board.is_valid(r, c, n):
                    board.grid[r][c] = n
                else:
                    print("Invalid move (conflict)")
                print_board(board)
            except:
                print("Usage: set r c n")

        elif cmd.startswith("hint"):
            try:
                _, r, c = cmd.split()
                r = int(r); c = int(c)
                if board.grid[r][c] != 0:
                    print("Cell is already filled.")
                    continue
                cand = board.candidates(r, c)
                print(f"Candidates at ({r},{c}): {cand}")
            except:
                print("Usage: hint r c")

        elif cmd == "show":
            print_board(board)

        elif cmd == "solve":
            print("Solving...")
            solver = SudokuBoard(board.grid)
            if solver.solve():
                board.grid = solver.grid
                print("Solution:")
                print_board(board)
            else:
                print("No solution found (should not happen).")

        elif cmd == "diff":
            print("Difficulty:", board.difficulty_rating())

        elif cmd == "quit":
            print("Goodbye!")
            break

        else:
            print("Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    start_game()
