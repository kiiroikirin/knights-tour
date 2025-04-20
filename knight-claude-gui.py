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
        self.solution = []

        # Size entry fields
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=5)
        
        tk.Label(size_frame, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Entry(size_frame, width=5)
        self.rows_entry.grid(row=0, column=1)
        self.rows_entry.insert(0, "8")
        
        tk.Label(size_frame, text="Columns:").grid(row=0, column=2)
        self.cols_entry = tk.Entry(size_frame, width=5)
        self.cols_entry.grid(row=0, column=3)
        self.cols_entry.insert(0, "8")
        
        tk.Button(size_frame, text="Set Size", command=self.set_board_size).grid(row=0, column=4, padx=5)

        self.setup_controls()

    def set_board_size(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if rows < 3 or cols < 3:
                print("Board must be at least 3x3")
                return
            self.initialize_board(rows, cols)
        except ValueError:
            print("Please enter valid numbers for rows and columns")

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        self.solve_button = tk.Button(control_frame, text="Select Start", command=self.enable_start_selection)
        self.solve_button.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.closed_tour_var = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="Closed Tour", variable=self.closed_tour_var).pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset_board)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.status_label = tk.Label(self.root, text="Select board size and click 'Select Start'")
        self.status_label.pack(pady=5)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        # default size
        self.initialize_board(8, 8)

    def initialize_board(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.knight = Knight(N=rows, M=cols)
        self.solution = []

        # Clear old buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                btn = tk.Button(self.board_frame, bg=GREEN, width=4, height=2, 
                                command=lambda r=row, c=col: self.handle_click(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                button_row.append(btn)
            self.buttons.append(button_row)

        self.update_board()
        self.status_label.config(text="Select board size and click 'Select Start'")
        self.solve_button.config(state='normal', text="Select Start")

    def reset_board(self):
        if self.knight:
            self.knight.board.reset()
            self.solution = []
            self.update_board()
            self.status_label.config(text="Board reset. Select 'Select Start' to begin.")
            self.solve_button.config(state='normal', text="Select Start")
            self.start_mode = False

    def enable_start_selection(self):
        self.start_mode = True
        self.status_label.config(text="Select a starting square")
        self.solve_button.config(state='disabled')

    def handle_click(self, row, col):
        if self.start_mode:
            self.start_mode = False
            self.status_label.config(text="Solving... please wait")
            self.root.update()
            
            # Reset board and set start position
            self.knight.board.reset()
            self.knight.set_start_position(row, col)
            self.update_board()
            
            # Attempt to solve
            closed_tour = self.closed_tour_var.get()
            self.root.after(100, lambda: self.solve_tour(closed_tour))
        else:
            self.status_label.config(text="Click 'Select Start' first to choose a starting position")

    def solve_tour(self, closed_tour):
        if closed_tour:
            success = self.knight.solve_closed_tour()
        else:
            success = self.knight.solve()
            
        if success:
            self.solution = self.knight.board.moves.copy()
            self.status_label.config(text=f"Solution found! Animating {len(self.solution)} moves...")
            self.animate_solution(0)
        else:
            self.status_label.config(text="No solution found from this starting position")
            self.solve_button.config(state='normal', text="Select Start")

    def animate_solution(self, move_index):
        if move_index >= len(self.solution):
            self.status_label.config(text="Solution complete!")
            self.solve_button.config(state='normal', text="Select Start")
            return
            
        # Clear board except for visited cells
        for row in range(self.rows):
            for col in range(self.cols):
                visited_up_to_now = False
                for i in range(move_index + 1):
                    if (row, col) == self.solution[i]:
                        visited_up_to_now = True
                        break
                        
                if visited_up_to_now:
                    self.buttons[row][col].config(bg=DARK_GREEN)
                else:
                    self.buttons[row][col].config(bg=GREEN)
                self.buttons[row][col].config(text="")
        
        # Show knight at current position
        current_x, current_y = self.solution[move_index]
        self.buttons[current_x][current_y].config(text="♞", fg=KNIGHT_COLOR, font=("Helvetica", 12, "bold"))
        
        # Show move number
        move_num = move_index
        if move_num > 0:
            self.buttons[current_x][current_y].config(text=f"♞\n{move_num}")
        
        # Schedule next animation step
        self.root.update()
        self.root.after(200, lambda: self.animate_solution(move_index + 1))

    def update_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.knight.board.get_cell(row, col)
                if cell and cell.visited:
                    self.buttons[row][col].config(bg=DARK_GREEN)
                else:
                    self.buttons[row][col].config(bg=GREEN)
                self.buttons[row][col].config(text="")
        
        # Show knight at current position if set
        if hasattr(self.knight.board, 'x') and hasattr(self.knight.board, 'y') and self.knight.board.moves:
            x, y = self.knight.board.x, self.knight.board.y
            self.buttons[x][y].config(text="♞", fg=KNIGHT_COLOR, font=("Helvetica", 12, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightsTourGUI(root)
    root.mainloop()