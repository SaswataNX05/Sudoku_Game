import threading
import time
import tkinter as tk
from tkinter import messagebox


class SudokuUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Auto Solver")
        self.root.resizable(False, False)

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.stop_requested = False
        self.is_running = False

        self._build_ui()
        self.load_sample()

    def _build_ui(self):
        header_frame = tk.Frame(self.root, pady=10)
        header_frame.pack()

        title_label = tk.Label(
            header_frame,
            text="SUDOKU SOLVER",
            font=("Helvetica", 16, "bold"),
            fg="#1f2937",
        )
        title_label.pack()

        self.status_label = tk.Label(
            header_frame,
            text="Status: Ready",
            font=("Helvetica", 10, "italic"),
            fg="#4b5563",
        )
        self.status_label.pack()

        grid_container = tk.Frame(
            self.root, bg="#111827", bd=3
        )
        grid_container.pack(padx=20, pady=5)

        for block_row in range(3):
            for block_col in range(3):
                block_frame = tk.Frame(
                    grid_container,
                    bg="#111827",
                    bd=1,
                    highlightbackground="#111827",
                    highlightthickness=1,
                )
                block_frame.grid(
                    row=block_row, column=block_col, padx=1, pady=1
                )

                for r in range(3):
                    for c in range(3):
                        actual_r = block_row * 3 + r
                        actual_c = block_col * 3 + c

                        cell = tk.Entry(
                            block_frame,
                            width=3,
                            font=("Helvetica", 16, "bold"),
                            justify="center",
                            bd=1,
                            relief="solid",
                            bg="#ffffff",
                            fg="#111827",
                        )
                        cell.grid(row=r, column=c, padx=1, pady=1, ipady=8)

                        vcmd = (
                            self.root.register(self._validate_input),
                            "%P",
                            "%d",
                        )
                        cell.config(validate="key", validatecommand=vcmd)

                        self.entries[actual_r][actual_c] = cell

        slider_frame = tk.Frame(self.root, pady=5)
        slider_frame.pack()

        tk.Label(
            slider_frame, text="Visualization Delay (ms):", font=("Helvetica", 9)
        ).pack(side=tk.LEFT, padx=5)
        self.delay_slider = tk.Scale(
            slider_frame,
            from_=0,
            to=150,
            orient=tk.HORIZONTAL,
            length=180,
            showvalue=True,
        )
        self.delay_slider.set(20)
        self.delay_slider.pack(side=tk.LEFT)

        btn_frame = tk.Frame(self.root, pady=15)
        btn_frame.pack()

        self.btn_instant = tk.Button(
            btn_frame,
            text="Solve Instant",
            bg="#2563eb",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=8,
            pady=4,
            relief="flat",
            command=lambda: self.start_solving(animated=False),
        )
        self.btn_instant.grid(row=0, column=0, padx=4)

        self.btn_visualize = tk.Button(
            btn_frame,
            text="Visualize Step",
            bg="#059669",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=8,
            pady=4,
            relief="flat",
            command=lambda: self.start_solving(animated=True),
        )
        self.btn_visualize.grid(row=0, column=1, padx=4)

        self.btn_sample = tk.Button(
            btn_frame,
            text="Load Sample",
            bg="#4b5563",
            fg="white",
            font=("Helvetica", 10),
            padx=8,
            pady=4,
            relief="flat",
            command=self.load_sample,
        )
        self.btn_sample.grid(row=0, column=2, padx=4)

        self.btn_clear = tk.Button(
            btn_frame,
            text="Clear",
            bg="#dc2626",
            fg="white",
            font=("Helvetica", 10),
            padx=8,
            pady=4,
            relief="flat",
            command=self.clear_board,
        )
        self.btn_clear.grid(row=0, column=3, padx=4)

    def _validate_input(self, proposed_text, action_type):
        if action_type == "0":
            return True
        return len(proposed_text) <= 1 and (
            proposed_text == "" or proposed_text in "123456789"
        )

    def get_matrix(self):
        matrix = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.entries[r][c].get().strip()
                row.append(int(val) if val.isdigit() else 0)
            matrix.append(row)
        return matrix

    def load_sample(self):
        if self.is_running:
            return
        sample = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        self.clear_board()
        for r in range(9):
            for c in range(9):
                if sample[r][c] != 0:
                    entry = self.entries[r][c]
                    entry.insert(0, str(sample[r][c]))
                    entry.config(
                        bg="#f3f4f6", fg="#111827"
                    )
        self.status_label.config(text="Status: Sample Loaded", fg="#4b5563")

    def clear_board(self):
        if self.is_running:
            self.stop_requested = True
            return
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                entry.config(state="normal", bg="#ffffff", fg="#111827")
                entry.delete(0, tk.END)
        self.status_label.config(text="Status: Board Cleared", fg="#4b5563")


    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False
        return True

    def find_empty(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return r, c
        return None

    def start_solving(self, animated=False):
        if self.is_running:
            return

        board = self.get_matrix()

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val != 0:
                    board[r][c] = 0
                    if not self.is_valid(board, r, c, val):
                        messagebox.showerror(
                            "Invalid Puzzle",
                            f"Initial board conflict at row {r+1}, col {c+1}.",
                        )
                        board[r][c] = val
                        return
                    board[r][c] = val

        self.is_running = True
        self.stop_requested = False
        self._toggle_buttons(disabled=True)
        self.status_label.config(
            text="Status: Solving...", fg="#2563eb"
        )

        # Run solver in background thread to prevent UI freezing
        threading.Thread(
            target=self._solve_thread,
            args=(board, animated),
            daemon=True,
        ).start()

    def _solve_thread(self, board, animated):
        delay = (self.delay_slider.get() / 1000.0) if animated else 0.0
        solved = self._backtrack(board, animated, delay)

        self.root.after(0, lambda: self._on_solve_complete(solved, board))

    def _backtrack(self, board, animated, delay):
        if self.stop_requested:
            return False

        empty = self.find_empty(board)
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num

                if animated:
                    self.root.after(
                        0, self._update_cell_ui, row, col, num, "#fef08a", "#2563eb"
                    )
                    time.sleep(delay)

                if self._backtrack(board, animated, delay):
                    return True

                board[row][col] = 0
                if animated:
                    self.root.after(
                        0, self._update_cell_ui, row, col, "", "#fee2e2", "#dc2626"
                    )
                    time.sleep(delay)

        return False

    def _update_cell_ui(self, r, c, val, bg_color, fg_color):
        entry = self.entries[r][c]
        entry.delete(0, tk.END)
        if val != "":
            entry.insert(0, str(val))
        entry.config(bg=bg_color, fg=fg_color)

    def _on_solve_complete(self, solved, board):
        self.is_running = False
        self._toggle_buttons(disabled=False)

        if solved:
            for r in range(9):
                for c in range(9):
                    entry = self.entries[r][c]
                    if entry.get() == "":
                        entry.insert(0, str(board[r][c]))
                    if entry.cget("bg") != "#f3f4f6":
                        entry.config(bg="#e0f2fe", fg="#0369a1")
            self.status_label.config(text="Status: Solved successfully!", fg="#059669")
        else:
            self.status_label.config(text="Status: No solution found", fg="#dc2626")
            if not self.stop_requested:
                messagebox.showinfo("Result", "No valid solution exists for this board.")

    def _toggle_buttons(self, disabled):
        state = tk.DISABLED if disabled else tk.NORMAL
        self.btn_instant.config(state=state)
        self.btn_visualize.config(state=state)
        self.btn_sample.config(state=state)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = SudokuUI(app_root)
    app_root.mainloop()
