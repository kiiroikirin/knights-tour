import tkinter as tk
import time
from knight import Knight

GREEN = "#90ee90"
DARK_GREEN = "#006400"
HIGHLIGHT = "#add8e6"
KNIGHT_COLOR = "#000000"

class KnightsTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Solver")
        self.solving = False
        self.start_mode = False

        self.knight = None
        self.rows = 0
        self.cols = 0
        self.buttons = []

        self.setup_controls()

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        self.solve_button = tk.Button(control_frame, text="Solve", command=self.enable_start_selection)
        self.solve_button.pack(pady=10)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        # default size
        self.initialize_board(8, 7)

    def initialize_board(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.knight = Knight(N=rows, M=cols)

        # Clear old buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                btn = tk.Button(self.board_frame, bg=GREEN, width=6, height=3,
                                command=lambda r=row, c=col: self.handle_click(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

        self.update_board()

    def enable_start_selection(self):
        self.start_mode = True
        self.solve_button.config(state='disabled')

    def handle_click(self, row, col):
        if self.start_mode:
            self.start_mode = False
            self.knight = Knight(N=self.rows, M=self.cols)
            self.knight.board.x = row
            self.knight.board.y = col
            self.knight.board.get_cell(row, col).mark_visited()
            self.knight.board.moves.append((row, col))
            self.animate_solution()
        else:
            print("Click 'Solve' and then select a starting square.")

    def animate_solution(self):
        if self.knight.solve_closed_tour():
            self.knight.board.printBoard()
            self.knight.board.printMoves()
            for i, (x, y) in enumerate(self.knight.board.moves):
                self.knight.board.get_cell(x, y).visited = True
                self.knight.board.x = x
                self.knight.board.y = y
                self.update_board()
                self.root.update()
                time.sleep(0.1)  # animation delay
        else:
            print("No solution found.")
        self.solve_button.config(state='normal')

    def update_board(self):
        knight_pos = (self.knight.board.x, self.knight.board.y)

        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.knight.board.get_cell(x, y)
                btn = self.buttons[x][y]

                if cell.visited:
                    btn.config(bg=DARK_GREEN)
                else:
                    btn.config(bg=GREEN)

                if (x, y) == knight_pos:
                    btn.config(text="♞", fg=KNIGHT_COLOR, font=("Helvetica", 12, "bold"))
                else:
                    btn.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightsTourGUI(root)
    root.mainloop()
