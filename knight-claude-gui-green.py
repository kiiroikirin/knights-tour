import tkinter as tk
import time
from knight import Knight

GREEN = "#90ee90"
DARK_GREEN = "#006400"
HIGHLIGHT = "#add8e6"
KNIGHT_COLOR = "#000000"
LIGHT_SQUARE = "#f0d9b5"  # Chess board light square
DARK_SQUARE = "#b58863"   # Chess board dark square

class KnightsTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Solver")
        self.solving = False
        self.start_mode = False
        self.player_mode = False

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
        
        self.player_button = tk.Button(control_frame, text="Play Mode", command=self.enter_player_mode)
        self.player_button.pack(side=tk.LEFT, padx=5, pady=10)
        
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
        self.player_mode = False

        # Clear old buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                # Alternating colors for chess-like pattern
                if (row + col) % 2 == 0:
                    bg_color = LIGHT_SQUARE
                else:
                    bg_color = DARK_SQUARE
                
                # Create button with coordinates
                btn = tk.Button(self.board_frame, bg=bg_color, width=6, height=3, 
                                command=lambda r=row, c=col: self.handle_click(r, c))
                
                # Add coordinate label
                btn.config(text=f"({row},{col})")
                
                btn.grid(row=row, column=col, padx=1, pady=1)
                button_row.append(btn)
            self.buttons.append(button_row)

        self.update_board()
        self.status_label.config(text="Select board size and click 'Select Start'")
        self.solve_button.config(state='normal', text="Select Start")
        self.player_button.config(state='normal')

    def reset_board(self):
        if self.knight:
            self.knight.board.reset()
            self.solution = []
            self.player_mode = False
            self.update_board()
            self.status_label.config(text="Board reset. Select 'Select Start' to begin.")
            self.solve_button.config(state='normal', text="Select Start")
            self.player_button.config(state='normal')
            self.start_mode = False

    def enable_start_selection(self):
        self.start_mode = True
        self.player_mode = False
        self.status_label.config(text="Select a starting square")
        self.solve_button.config(state='disabled')
        self.player_button.config(state='disabled')

    def enter_player_mode(self):
        self.player_mode = True
        self.start_mode = True
        self.status_label.config(text="Player Mode: Select a starting square")
        self.solve_button.config(state='disabled')
        self.player_button.config(state='disabled')

    def handle_click(self, row, col):
        if self.start_mode:
            # First click - set starting position
            self.knight.board.reset()
            self.knight.set_start_position(row, col)
            self.update_board()
            
            if self.player_mode:
                # Continue in player mode
                self.start_mode = False
                self.status_label.config(text="Player Mode: Make your moves by clicking valid squares")
            else:
                # Solver mode
                self.start_mode = False
                self.status_label.config(text="Solving... please wait")
                self.root.update()
                
                # Attempt to solve
                closed_tour = self.closed_tour_var.get()
                self.root.after(100, lambda: self.solve_tour(closed_tour))
        
        elif self.player_mode:
            # Player is making moves
            success = self.knight.move(row, col)
            if success:
                # Valid move made
                self.update_board(highlight_last=True)
                
                # Check if all cells are visited
                all_visited = True
                for r in range(self.rows):
                    for c in range(self.cols):
                        if not self.knight.board.get_cell(r, c).visited:
                            all_visited = False
                            break
                    if not all_visited:
                        break
                
                if all_visited:
                    self.status_label.config(text="Congratulations! You completed the knight's tour!")
                    self.solve_button.config(state='normal', text="Select Start")
                    self.player_button.config(state='normal')
                    self.player_mode = False
                else:
                    available_moves = self.knight.board.get_available_moves()
                    if not available_moves:
                        self.status_label.config(text="No more valid moves! Game over.")
                        self.solve_button.config(state='normal', text="Select Start")
                        self.player_button.config(state='normal')
                        self.player_mode = False
                    else:
                        self.status_label.config(text=f"Player Mode: {len(available_moves)} valid moves available")
            else:
                self.status_label.config(text="Invalid move! Knight must move in L-shape to unvisited square")
        
        else:
            self.status_label.config(text="Click 'Select Start' or 'Play Mode' first")

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
            self.player_button.config(state='normal')

    def animate_solution(self, move_index):
        if move_index >= len(self.solution):
            self.status_label.config(text="Solution complete!")
            self.solve_button.config(state='normal', text="Select Start")
            self.player_button.config(state='normal')
            return
            
        # Update board to show current state
        self.update_solution_board(move_index)
        
        # Schedule next animation step
        self.root.update()
        self.root.after(200, lambda: self.animate_solution(move_index + 1))

    def update_solution_board(self, move_index):
        # Reset all cells to their original color, keeping coordinates visible
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    self.buttons[row][col].config(bg=LIGHT_SQUARE)
                else:
                    self.buttons[row][col].config(bg=DARK_SQUARE)
                
                self.buttons[row][col].config(text=f"({row},{col})")
        
        # Color all visited cells green
        for i in range(move_index + 1):
            x, y = self.solution[i]
            # Intensity of green depends on when it was visited
            intensity = max(50, 255 - int(200 * i / (len(self.solution) - 1))) if len(self.solution) > 1 else 150
            green_color = f"#{0:02x}{intensity:02x}{0:02x}"
            self.buttons[x][y].config(bg=green_color, text=f"({x},{y})\n{i}")
        
        # Show knight at current position
        current_x, current_y = self.solution[move_index]
        self.buttons[current_x][current_y].config(text=f"({current_x},{current_y})\n♞\n{move_index}")

    def update_board(self, highlight_last=False):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.knight.board.get_cell(row, col)
                
                # Keep the coordinates visible
                coord_text = f"({row},{col})"
                
                if cell and cell.visited:
                    # Green for visited cells, showing coordinates
                    self.buttons[row][col].config(bg=GREEN, text=coord_text)
                else:
                    # Original chess pattern for unvisited
                    if (row + col) % 2 == 0:
                        self.buttons[row][col].config(bg=LIGHT_SQUARE, text=coord_text)
                    else:
                        self.buttons[row][col].config(bg=DARK_SQUARE, text=coord_text)
        
        # Show knight at current position
        if self.knight and self.knight.board.moves:
            x, y = self.knight.board.x, self.knight.board.y
            
            # For the last move in player mode, use darker green
            if highlight_last and self.player_mode:
                self.buttons[x][y].config(bg=DARK_GREEN)
            
            # Show knight symbol with coordinates
            self.buttons[x][y].config(text=f"({x},{y})\n♞")
            
            # If in player mode, highlight available moves
            if self.player_mode:
                available_moves = self.knight.board.get_available_moves()
                for move_x, move_y in available_moves:
                    self.buttons[move_x][move_y].config(bg=HIGHLIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightsTourGUI(root)
    root.mainloop()