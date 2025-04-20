"""knights.py
a program to solve an NxM knights tour board
input: starting square
output: sequence of moves
"""

class Cell:
    def __init__(self, x, y):
        """Represents a cell on the board"""
        self.x = x
        self.y = y
        self.visited = False

    def mark_visited(self):
        """Mark the cell as visited"""
        self.visited = True

    def __str__(self):
        """String representation of the cell"""
        return 'X' if self.visited else '.'

    def is_knight_move(self, knight):
        """Check if the cell is a valid knight's move from knight's position"""
        dx = abs(knight.x - self.x)
        dy = abs(knight.y - self.y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

class Board:
    def __init__(self, rows, cols, start_x=0, start_y=0):
        """create a board of size NxM"""
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.x = start_x  # knight's x coordinate
        self.y = start_y  # knight's y coordinate
        self.start_x = start_x  # remember starting position for closed tour
        self.start_y = start_y
        self.moveCount = 0
        self.board[self.x][self.y].mark_visited()
        self.moves = [(self.x, self.y)]  # Include starting position in moves
    
    def get_cell(self, x, y):
        """Retrieve a specific cell on the board"""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.board[x][y]
        else:
            return None  # Return None for out of bounds instead of raising error

    def check_move(self, x, y):
        """Check if the knight can move to a specific cell"""
        cell = self.get_cell(x, y)
        if cell is None:
            return False
        if cell.visited:
            return False
        
        # Check if this is a valid knight's move
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
    
    def get_available_moves(self):
        """Get all available moves for the knight"""
        moves = []
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols and not self.board[new_x][new_y].visited:
                moves.append((new_x, new_y))
        return moves

    def get_available_moves_from(self, cell):
        """Get all available moves from a specific cell"""
        moves = []
        x, y = cell
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols and not self.board[new_x][new_y].visited:
                moves.append((new_x, new_y))
        return moves

    def printBoard(self):
        """print the board"""
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print(f"Knight position: ({self.x}, {self.y})")
        print(f"Moves available: {len(self.get_available_moves())} and they are {self.get_available_moves()}")
    
    def isSolved(self, tour=False):
        """check if the board is solved"""
        # Check if all cells have been visited
        all_visited = True
        for row in self.board:
            for cell in row:
                if not cell.visited:
                    all_visited = False
                    break
            if not all_visited:
                break
        
        # If we're checking for a closed tour, make sure we can return to start
        if tour and all_visited:
            # Check if the current position can reach the starting position
            dx = abs(self.x - self.start_x)
            dy = abs(self.y - self.start_y)
            can_return = (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
            return can_return
        
        return all_visited
    
    def undo_move(self):
        """undo the knight's last move"""
        if len(self.moves) <= 1:  # Don't remove the starting position
            return False
        
        self.moves.pop()  # Remove current position
        prev_x, prev_y = self.moves[-1]  # Get the previous position
        
        self.board[self.x][self.y].visited = False
        self.x, self.y = prev_x, prev_y
        self.moveCount -= 1
        
        return True

    def move(self, x, y):
        """move the knight to a new square"""
        if not self.check_move(x, y):
            return False
        
        self.x = x
        self.y = y
        self.moveCount += 1
        self.board[x][y].mark_visited()
        self.moves.append((x, y))
        
        return True

    def printMoves(self):
        """print the moves made by the knight"""
        print("Moves made:")
        indexed_moves = zip(range(len(self.moves)), self.moves)
        print(list(indexed_moves))
        print(f"Total moves: {self.moveCount}")

class Knight:
    def __init__(self, N=8, M=7, start_x=0, start_y=0):
        self.board = Board(N, M, start_x, start_y)

    def move(self, x, y):
        """move the knight to a new square"""
        return self.board.move(x, y)

    def encode_board(self):
        """encodes the board state as a string"""
        board_str = ""
        for row in self.board.board:
            for cell in row:
                board_str += "1" if cell.visited else "0"
        return board_str
        
    def solve(self, tour=False):
        """solve the knights tour using Warnsdorff's heuristic"""
        # Check if we've already visited all cells
        total_cells = self.board.rows * self.board.cols
        
        if self.board.moveCount == total_cells - 1:
            # We've visited all cells except the current one
            if not tour or self.board.isSolved(tour):
                return True
            return False
        
        # Warnsdorff's heuristic: sort moves by number of onward moves (fewer first)
        moves = self.board.get_available_moves()
        if not moves:
            return False
            
        # Sort by the number of onward moves (fewer options first)
        moves.sort(key=lambda move: len(self.board.get_available_moves_from(move)))
        
        for move_x, move_y in moves:
            if self.board.move(move_x, move_y):
                if self.solve(tour):
                    return True
                self.board.undo_move()
        
        return False

    def solve_closed_tour(self):
        """Specifically solve for a closed knights tour"""
        return self.solve(tour=True)

if __name__ == '__main__':
    # Create a knight on a 7x8 board
    player = Knight(7, 8)
    print("Initial board:")
    player.board.printBoard()
    
    #print("\nSolving for closed tour...")
    #found = player.solve_closed_tour()
    
    print("\nSolving for any tour...")
    found = player.solve()

    print("\nFinal board:")
    player.board.printBoard()
    
    if found:
        print("\nSolution found!")
        player.board.printMoves()
    else:
        print("\nNo solution found for a closed tour from the starting position")