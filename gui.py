import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import json
import copy
import threading
import os

from sudoku import SudokuBoard, generate, generate_unique

# ---------- 常數 ----------
CELL_SIZE = 48
FONT = ("Consolas", 18)
NOTE_FONT = ("Consolas", 10)
GIVEN_BG = "#E8E8E8"
USER_BG = "white"
CONFLICT_BG = "#FFB3B3"
SELECT_BG = "#D7F0FF"
NOTE_FG = "#6B6B6B"

SAVE_FILE_EXT = [("Sudoku JSON", "*.json"), ("All files", "*.*")]

# ---------- GUI 主視窗 ----------
class SudokuGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku GUI")
        self.resizable(False, False)

        # 狀態
        self.board = None               # SudokuBoard current numeric grid
        self.solution = None
        self.givens = [[0]*9 for _ in range(9)]  # givens grid: 0 = editable
        self.notes = [[set() for _ in range(9)] for __ in range(9)]  # notes as sets of ints
        self.entries = [[None]*9 for _ in range(9)]
        self.selected = None            # (r,c)
        self.undo_stack = []            # list of actions
        self.redo_stack = []
        self.mode = "NORMAL"   # NORMAL or NOTES
        self.notes_mode = False         # true = input toggles notes
        self._build_ui()
        # default new puzzle
        self.new_puzzle_dialog(initial=True)

    # ---------- UI 組件 ----------
    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(padx=8, pady=6)

        # Board frame (use Frame + Entry)
        board_frame = tk.Frame(top)
        board_frame.grid(row=0, column=0, rowspan=12)

        for r in range(9):
            for c in range(9):
                # use a Frame containing an Entry for flexibility
                f = tk.Frame(board_frame, width=CELL_SIZE, height=CELL_SIZE)
                f.grid_propagate(False)
                f.grid(row=r, column=c, padx=(0 if c%3!=0 else 4), pady=(0 if r%3!=0 else 4))
                e = tk.Entry(f, justify="center", font=FONT)
                e.place(relwidth=1, relheight=1)
                # Bindings: focus, key, click
                e.bind("<FocusIn>", lambda ev, rr=r, cc=c: self._on_select(rr, cc))
                e.bind("<KeyRelease>", lambda ev, rr=r, cc=c: self._on_key(rr, cc, ev))
                e.bind("<Button-1>", lambda ev, rr=r, cc=c: self._on_select(rr, cc))
                self.entries[r][c] = e

        # Controls
        controls = tk.Frame(top)
        controls.grid(row=0, column=1, sticky="nw", padx=8)

        btn_new = tk.Button(controls, text="New Puzzle", width=20, command=lambda: self.new_puzzle_dialog())
        btn_new.grid(row=0, column=0, pady=2)

        btn_notes = tk.Button(controls, text="Toggle Notes: OFF", width=20, command=self.toggle_notes_mode)
        btn_notes.grid(row=1, column=0, pady=2)
        self.btn_notes = btn_notes

        btn_hint = tk.Button(controls, text="Hint", width=20, command=self.hint)
        btn_hint.grid(row=2, column=0, pady=2)

        btn_solve = tk.Button(controls, text="Solve", width=20, command=self.solve)
        btn_solve.grid(row=3, column=0, pady=2)

        btn_check = tk.Button(controls, text="Check", width=20, command=self.check_board)
        btn_check.grid(row=4, column=0, pady=2)

        btn_diff = tk.Button(controls, text="Difficulty", width=20, command=self.show_difficulty)
        btn_diff.grid(row=5, column=0, pady=2)

        undo_frame = tk.Frame(controls)
        undo_frame.grid(row=6, column=0, pady=2)
        btn_undo = tk.Button(undo_frame, text="Undo", width=9, command=self.undo)
        btn_undo.pack(side="left", padx=2)
        btn_redo = tk.Button(undo_frame, text="Redo", width=9, command=self.redo)
        btn_redo.pack(side="left", padx=2)

        save_frame = tk.Frame(controls)
        save_frame.grid(row=7, column=0, pady=2)
        btn_save = tk.Button(save_frame, text="Save", width=9, command=self.save)
        btn_save.pack(side="left", padx=2)
        btn_load = tk.Button(save_frame, text="Load", width=9, command=self.load)
        btn_load.pack(side="left", padx=2)

        lbl = tk.Label(controls, text="\nInstructions:\n- Click cell and type 1-9\n- Backspace or 0 clears\n- In Notes mode, typing toggles note\n- Givens are locked (gray)")
        lbl.grid(row=8, column=0, pady=6)

    # ---------- New puzzle dialog (difficulty selection) ----------
    def new_puzzle_dialog(self, initial=False):
        # custom Toplevel dialog to choose difficulty and unique
        def on_ok():
            sel = var.get()
            unique = var_unique.get()
            if sel == "Easy":
                holes = 30
            elif sel == "Medium":
                holes = 40
            elif sel == "Hard":
                holes = 50
            elif sel == "Expert":
                holes = 60
            elif sel == "Custom":
                val = ent_custom.get().strip()
                try:
                    holes = int(val)
                    if not (0 <= holes <= 64):
                        messagebox.showerror("Error", "Custom holes must be 0..64")
                        return
                except:
                    messagebox.showerror("Error", "Custom holes must be an integer")
                    return
            else:
                holes = 40
            dialog.destroy()
            if unique:
                self._start_new_unique(holes)
            else:
                self.new_puzzle(holes, unique=False)

        dialog = tk.Toplevel(self)
        dialog.title("New Puzzle")
        dialog.transient(self)
        dialog.grab_set()
        tk.Label(dialog, text="Select difficulty:").pack(padx=10, pady=6)
        var = tk.StringVar(value="Medium")
        for name in ("Easy","Medium","Hard","Expert","Custom"):
            tk.Radiobutton(dialog, text=name, variable=var, value=name).pack(anchor="w", padx=14)

        ent_custom = tk.Entry(dialog)
        tk.Label(dialog, text="Custom holes (only for Custom above):").pack(padx=10, pady=(8,0))
        ent_custom.pack(padx=10, pady=(0,8))
        var_unique = tk.BooleanVar(value=False)
        tk.Checkbutton(dialog, text="Require unique solution (slower)", variable=var_unique).pack(padx=10, pady=6)

        btn = tk.Button(dialog, text="OK", command=on_ok)
        btn.pack(pady=8)
        if initial:
            # if initial call, pick Medium default and close automatically
            dialog.destroy()
            self.new_puzzle(40, unique=False)

    # ---------- Puzzle 管理 ----------
    def new_puzzle(self, holes=40, unique=False):
        # generate puzzle (unique may be slow)
        if unique:
            puzzle, solution = generate_unique(holes)
        else:
            puzzle, solution = generate(holes)
        self.solution = solution
        self.board = SudokuBoard(puzzle.grid)

            # RESET mode
        self.notes_mode = False
        self.mode = "NORMAL"
        self.btn_notes.config(text="Toggle Notes: OFF")
        # givens = where puzzle had numbers
        for r in range(9):
            for c in range(9):
                val = puzzle.grid[r][c]
                self.givens[r][c] = val
                self.notes[r][c].clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self._refresh_ui()
        self._highlight_conflicts()

    def _start_new_unique(self, holes):
        # generate unique might take time; use threading so UI not freeze
        def job():
            try:
                self._set_status("Generating unique puzzle (may take a while)...")
                puzzle, solution = generate_unique(holes)
                self.solution = solution
                self.board = SudokuBoard(puzzle.grid)
                # RESET mode
                self.notes_mode = False
                self.mode = "NORMAL"
                self.btn_notes.config(text="Toggle Notes: OFF")

                for r in range(9):
                    for c in range(9):
                        self.givens[r][c] = puzzle.grid[r][c]
                        self.notes[r][c].clear()
                self.undo_stack.clear()
                self.redo_stack.clear()
                self._refresh_ui()
                self._highlight_conflicts()
                self._set_status("")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate unique puzzle: {e}")
                self._set_status("")
        t = threading.Thread(target=job, daemon=True)
        t.start()

    # ---------- UI 更新 ----------
    def _refresh_ui(self):
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                val = self.board.grid[r][c] if self.board else 0
                if self.givens[r][c] != 0:
                    e.config(state="normal")
                    e.delete(0, tk.END)
                    e.insert(0, str(self.givens[r][c]))
                    e.config(state="disabled", disabledforeground="black", disabledbackground=GIVEN_BG)
                else:
                    e.config(state="normal", fg="black", font=FONT)
                    e.delete(0, tk.END)
                    if val != 0:
                        e.insert(0, str(val))
                    else:
                        # if notes exist show as concatenated string in gray
                        notes = sorted(self.notes[r][c])
                        if notes:
                            e.insert(0, "".join(str(x) for x in notes))
                            e.config(fg=NOTE_FG, font=NOTE_FONT)
                        else:
                            e.config(fg="black", font=FONT)
                    e.config(bg=USER_BG)

    def _set_status(self, text):
        self.title(f"Sudoku GUI - {text}" if text else "Sudoku GUI")

    # ---------- Selection / Input ----------
    def _on_select(self, r, c):
        prev = self.selected
        self.selected = (r, c)
        for rr in range(9):
            for cc in range(9):
                e = self.entries[rr][cc]
                if (rr,cc) == (r,c):
                    e.config(bg=SELECT_BG)
                else:
                    if self.givens[rr][cc] != 0:
                        e.config(state="disabled", disabledbackground=GIVEN_BG)
                    else:
                        e.config(state="normal", bg=USER_BG)
        # focus selected entry
        self.entries[r][c].focus_set()

    def _on_key(self, r, c, event):
        e = self.entries[r][c]
        txt = e.get().strip()
        # deletion
        if txt == "" or txt == "0":
            # clear value or notes
            old_val = self.board.grid[r][c]
            old_notes = set(self.notes[r][c])
            if self.givens[r][c] != 0:
                # reset to given
                e.delete(0, tk.END)
                e.insert(0, str(self.givens[r][c]))
                e.config(state="disabled", disabledforeground="black", disabledbackground=GIVEN_BG)
                return
            # clear both
            if old_val != 0 or old_notes:
                self._push_undo_full(r,c, old_val, 0, old_notes, set())
                self.board.grid[r][c] = 0
                self.notes[r][c].clear()
                e.delete(0, tk.END)
            self._highlight_conflicts()
            return

        # only last char matters
        if len(txt) > 1:
            txt = txt[-1]
            e.delete(0, tk.END)
            e.insert(0, txt)
        if not txt.isdigit() or not (1 <= int(txt) <= 9):
            e.delete(0, tk.END)
            # if previous notes exist re-show them
            if self.board.grid[r][c] == 0 and self.notes[r][c]:
                e.insert(0, "".join(str(x) for x in sorted(self.notes[r][c])))
                e.config(fg=NOTE_FG, font=NOTE_FONT)
            return

        num = int(txt)

        if self.givens[r][c] != 0:
            # cannot change given
            e.delete(0, tk.END)
            e.insert(0, str(self.givens[r][c]))
            e.config(state="disabled", disabledforeground="black", disabledbackground=GIVEN_BG)
            return

        # NOTES MODE
        if self.notes_mode:
            # toggle note
            old_val = self.board.grid[r][c]
            old_notes = set(self.notes[r][c])
            if num in self.notes[r][c]:
                self.notes[r][c].remove(num)
            else:
                self.notes[r][c].add(num)
            # update UI: if there is a real value, keep it; else show notes
            if self.board.grid[r][c] != 0:
                e.delete(0, tk.END)
                e.insert(0, str(self.board.grid[r][c]))
                e.config(fg="black", font=FONT)
            else:
                e.delete(0, tk.END)
                notes_sorted = sorted(self.notes[r][c])
                if notes_sorted:
                    e.insert(0, "".join(str(x) for x in notes_sorted))
                    e.config(fg=NOTE_FG, font=NOTE_FONT)
                else:
                    e.config(fg="black", font=FONT)
            self._push_undo_full(r,c, old_val, old_val, old_notes, set(self.notes[r][c]))
            return

        # NORMAL MODE: place a number
        old_val = self.board.grid[r][c]
        old_notes = set(self.notes[r][c])
        self.board.grid[r][c] = num
        # when a digit placed, clear notes for that cell
        self.notes[r][c].clear()
        # update UI
        e.delete(0, tk.END)
        e.insert(0, str(num))
        e.config(fg="black", font=FONT)
        self._push_undo_full(r,c, old_val, num, old_notes, set())
        # highlight conflicts
        self._highlight_conflicts()
        # check completion
        if self._is_complete():
            messagebox.showinfo("Solved", "Congratulations! Puzzle appears complete.")
            if self.solution:
                if all(self.board.grid[rr][cc] == self.solution.grid[rr][cc] for rr in range(9) for cc in range(9)):
                    messagebox.showinfo("Correct", "Solution matches generator's solution.")
                else:
                    messagebox.showwarning("Note", "Complete but differs from generator solution (puzzle may have multiple solutions).")

    # ---------- Undo/Redo (full with notes) ----------
    def _push_undo_full(self, r, c, old_val, new_val, old_notes, new_notes):
        # store as tuple; new_val could equal old_val when only notes changed
        self.undo_stack.append((r, c, old_val, new_val, set(old_notes), set(new_notes)))
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        r,c,old_val,new_val,old_notes,new_notes = self.undo_stack.pop()
        # compute current state to push to redo
        cur_val = self.board.grid[r][c]
        cur_notes = set(self.notes[r][c])
        self.redo_stack.append((r,c,cur_val,old_val,set(cur_notes),set(old_notes)))
        # restore
        self.board.grid[r][c] = old_val
        self.notes[r][c] = set(old_notes)
        e = self.entries[r][c]
        e.config(state="normal")
        e.delete(0, tk.END)
        if self.givens[r][c] != 0:
            e.insert(0, str(self.givens[r][c]))
            e.config(state="disabled", disabledforeground="black", disabledbackground=GIVEN_BG)
        else:
            if old_val != 0:
                e.insert(0, str(old_val))
                e.config(fg="black", font=FONT)
            else:
                notes_sorted = sorted(self.notes[r][c])
                if notes_sorted:
                    e.insert(0, "".join(str(x) for x in notes_sorted))
                    e.config(fg=NOTE_FG, font=NOTE_FONT)
                else:
                    e.config(fg="black", font=FONT)
        self._highlight_conflicts()

    def redo(self):
        if not self.redo_stack:
            return
        r,c,cur_val,redo_val,cur_notes,redo_notes = self.redo_stack.pop()
        # push to undo
        self.undo_stack.append((r,c,self.board.grid[r][c],redo_val,set(self.notes[r][c]),set(redo_notes)))
        self.board.grid[r][c] = redo_val
        self.notes[r][c] = set(redo_notes)
        e = self.entries[r][c]
        e.config(state="normal")
        e.delete(0, tk.END)
        if self.givens[r][c] != 0:
            e.insert(0, str(self.givens[r][c]))
            e.config(state="disabled", disabledforeground="black", disabledbackground=GIVEN_BG)
        else:
            if redo_val != 0:
                e.insert(0, str(redo_val))
                e.config(fg="black", font=FONT)
            else:
                notes_sorted = sorted(self.notes[r][c])
                if notes_sorted:
                    e.insert(0, "".join(str(x) for x in notes_sorted))
                    e.config(fg=NOTE_FG, font=NOTE_FONT)
                else:
                    e.config(fg="black", font=FONT)
        self._highlight_conflicts()

    # ---------- Highlight conflicts ----------
    def _highlight_conflicts(self):
        # reset all
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                if self.givens[r][c] != 0:
                    e.config(state="disabled", disabledbackground=GIVEN_BG)
                else:
                    e.config(state="normal", bg=USER_BG, fg="black", font=FONT)
        # check each filled numeric cell for conflicts; mark background red if conflict
        for r in range(9):
            for c in range(9):
                val = self.board.grid[r][c]
                if val == 0:
                    # if notes exist, show them in gray
                    e = self.entries[r][c]
                    notes_sorted = sorted(self.notes[r][c])
                    e.config(state="normal")
                    e.delete(0, tk.END)
                    if notes_sorted:
                        e.insert(0, "".join(str(x) for x in notes_sorted))
                        e.config(fg=NOTE_FG, font=NOTE_FONT)
                    continue
                # Temporarily remove current cell and check validity
                saved = self.board.grid[r][c]
                self.board.grid[r][c] = 0
                ok = self.board.is_valid(r, c, saved)
                self.board.grid[r][c] = saved
                if not ok:
                    e = self.entries[r][c]
                    e.config(bg=CONFLICT_BG)

    # ---------- Helpers ----------
    def _is_complete(self):
        # no zeros and no conflicts: check values & validity
        for r in range(9):
            for c in range(9):
                if self.board.grid[r][c] == 0:
                    return False
        # check each cell validity
        for r in range(9):
            for c in range(9):
                v = self.board.grid[r][c]
                saved = self.board.grid[r][c]
                self.board.grid[r][c] = 0
                ok = self.board.is_valid(r, c, saved)
                self.board.grid[r][c] = saved
                if not ok:
                    return False
        return True

    # ---------- Hint ----------
    def hint(self):
        if not self.selected:
            messagebox.showinfo("Hint", "Select a cell first.")
            return
        r,c = self.selected
        if self.givens[r][c] != 0:
            messagebox.showinfo("Hint", "This is a given clue.")
            return
        cand = self.board.candidates(r,c)
        messagebox.showinfo("Candidates", f"Candidates for ({r},{c}): {cand}")

    # ---------- Solve (auto) ----------
    def solve(self):
        copy_board = SudokuBoard([row[:] for row in self.board.grid])
        if copy_board.solve():
            # apply solution to UI, but keep givens immutable
            for r in range(9):
                for c in range(9):
                    if self.givens[r][c] == 0:
                        val = copy_board.grid[r][c]
                        self.board.grid[r][c] = val
                        self.notes[r][c].clear()
                        e = self.entries[r][c]
                        e.config(state="normal")
                        e.delete(0, tk.END)
                        if val != 0:
                            e.insert(0, str(val))
                            e.config(fg="black", font=FONT)
            self._highlight_conflicts()
            messagebox.showinfo("Solved", "Auto-solve finished.")
        else:
            messagebox.showwarning("No solution", "This puzzle is unsolvable.")

    # ---------- Check (validate) ----------
    def check_board(self):
        # Check that current board has no conflicts and is valid partial board
        try:
            tmp = SudokuBoard([row[:] for row in self.board.grid])
            messagebox.showinfo("Check", "Board is currently valid (no duplicate givens).")
        except Exception as e:
            messagebox.showerror("Invalid", f"Board is invalid: {e}")

    # ---------- Difficulty ----------
    def show_difficulty(self):
        try:
            d = self.board.difficulty_rating()
            messagebox.showinfo("Difficulty", f"Difficulty: {d}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to evaluate difficulty: {e}")

    # ---------- Notes mode toggle ----------
    def toggle_notes_mode(self):
        self.notes_mode = not self.notes_mode
        self.mode = "NOTES" if self.notes_mode else "NORMAL"
        self.btn_notes.config(text=f"Toggle Notes: {'ON' if self.notes_mode else 'OFF'}")

    # ---------- Save / Load ----------
    def save(self):
        # Save current puzzle state (givens + current values + notes)
        data = {
            "givens": self.givens,
            "grid": self.board.grid,
            "notes": [[sorted(list(s)) for s in row] for row in self.notes]
        }
        fpath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=SAVE_FILE_EXT)
        if not fpath:
            return
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", f"Saved to {fpath}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def load(self):
        fpath = filedialog.askopenfilename(filetypes=SAVE_FILE_EXT)
        if not fpath:
            return
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            givens = data.get("givens")
            grid = data.get("grid")
            notes_data = data.get("notes", None)
            if not givens or not grid:
                messagebox.showerror("Load error", "File missing required fields.")
                return
            # validate shapes
            if not (len(givens) == 9 and len(grid) == 9):
                messagebox.showerror("Load error", "Invalid grid size.")
                return
            self.givens = givens
            self.board = SudokuBoard(grid)
            # load notes
            if notes_data:
                for r in range(9):
                    for c in range(9):
                        self.notes[r][c] = set(notes_data[r][c])
            else:
                self.notes = [[set() for _ in range(9)] for __ in range(9)]
            self.solution = None
            self.notes_mode = False
            self.mode = "NORMAL"
            self.btn_notes.config(text="Toggle Notes: OFF")
            self.undo_stack.clear()
            self.redo_stack.clear()
            self._refresh_ui()
            self._highlight_conflicts()
            messagebox.showinfo("Loaded", f"Loaded {os.path.basename(fpath)}")
        except Exception as e:
            messagebox.showerror("Load error", str(e))


if __name__ == "__main__":
    app = SudokuGUI()
    app.mainloop()
