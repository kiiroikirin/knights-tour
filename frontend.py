import tkinter as tk
from knight import Knight  # Assumes your code is saved in knights.py

# Colors
GREEN = "#90ee90"
DARK_GREEN = "#006400"
HIGHLIGHT = "#add8e6"

class KnightsTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Game")

        self.knight = Knight()
        self.rows = self.knight.board.rows
        self.cols = self.knight.board.cols

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_board()
        self.update_board()

    def create_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                btn = tk.Button(self.root, bg=GREEN, width=6, height=3,
                                command=lambda r=row, c=col: self.handle_click(r, c))
                # Set the button's text to show the cell coordinates
                btn.config(text=f"({row}, {col})")
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def handle_click(self, row, col):
        valid_moves = self.knight.board.get_available_moves()
        print(f"Valid moves: {valid_moves}")
        if (row, col) in valid_moves:
            self.knight.move(row, col)
            self.update_board()
        else:
            print(f"Invalid move from ({self.knight.board.rows}, {self.knight.board.cols}) to ({row}, {col})")

    def update_board(self):
        available_moves = self.knight.board.get_available_moves()
        knight_pos = (self.knight.board.x, self.knight.board.y)

        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.knight.board.get_cell(x, y)
                btn = self.buttons[x][y]

                # Set tile color
                if cell.visited:
                    btn.config(bg=DARK_GREEN)
                elif (x, y) in available_moves:
                    btn.config(bg=HIGHLIGHT)
                else:
                    btn.config(bg=GREEN)

                # Set knight symbol
                if (x, y) == knight_pos:
                    btn.config(text="♞", fg="black", font=("Helvetica", 12, "bold"))
                else:
                    btn.config(text=f"({x}, {y})")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightsTourGUI(root)
    root.mainloop()
