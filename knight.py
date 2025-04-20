"""knight.py
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

    def is_knight_move(self, x, y):
        """Check if the cell is a valid knight's move from given position"""
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

class Board:
    def __init__(self, rows, cols):
        """create a board of size NxM"""
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.x = 0  # knight's x coordinate
        self.y = 0  # knight's y coordinate
        self.start_x = 0  # starting position for closed tour
        self.start_y = 0
        self.moveCount = 0
        self.moves = []  # Don't add starting position yet
    
    def set_start_position(self, x, y):
        """Set the starting position of the knight"""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.x = x
            self.y = y
            self.start_x = x
            self.start_y = y
            self.board[x][y].mark_visited()
            self.moves = [(x, y)]  # Set starting position
            self.moveCount = 0
            return True
        return False
    
    def get_cell(self, x, y):
        """Retrieve a specific cell on the board"""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.board[x][y]
        else:
            return None  # Return None for out of bounds
    
    def get_available_moves(self):
        """Get all available moves for the knight"""
        moves = []
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols and not self.board[new_x][new_y].visited:
                moves.append((new_x, new_y))
        return moves

    def get_available_moves_from(self, pos):
        """Get all available moves from a specific position"""
        x, y = pos
        moves = []
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
    
    def reset(self):
        """Reset the board"""
        for row in self.board:
            for cell in row:
                cell.visited = False
        self.moveCount = 0
        self.moves = []
    
    def undo_move(self):
        """undo the knight's last move"""
        if len(self.moves) <= 1:  # Don't remove the starting position
            return False
        
        self.board[self.x][self.y].visited = False
        self.moves.pop()  # Remove current position
        self.x, self.y = self.moves[-1]  # Get the previous position
        self.moveCount -= 1
        
        return True

    def move(self, x, y):
        """move the knight to a new square"""
        # Check if in bounds
        if not (0 <= x < self.rows and 0 <= y < self.cols):
            return False
            
        # Check if unvisited
        if self.board[x][y].visited:
            return False
            
        # Check if valid knight move
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        if not ((dx == 2 and dy == 1) or (dx == 1 and dy == 2)):
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
    def __init__(self, N=8, M=7):
        self.board = Board(N, M)

    def set_start_position(self, x, y):
        """Set the starting position for the knight"""
        return self.board.set_start_position(x, y)

    def move(self, x, y):
        """move the knight to a new square"""
        return self.board.move(x, y)
        
    def solve_closed_tour(self):
        """Solve for a closed knight's tour"""
        # Check if start position has been set
        if not self.board.moves:
            return False
            
        return self._solve(True)
    
    def solve(self):
        """Solve for an open knight's tour"""
        # Check if start position has been set
        if not self.board.moves:
            return False
            
        return self._solve(False)
        
    def _solve(self, tour=False):
        """Solve the knight's tour using Warnsdorff's heuristic"""
        # Check if we've visited all cells
        total_cells = self.board.rows * self.board.cols
        
        if self.board.moveCount == total_cells - 1:
            # We're visiting the last cell
            if not tour:
                return True
                
            # For closed tour, check if we can get back to start
            last_x, last_y = self.board.x, self.board.y
            dx = abs(last_x - self.board.start_x)
            dy = abs(last_y - self.board.start_y)
            if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
                return True
            return False
        
        # Warnsdorff's heuristic: sort moves by fewest onward moves
        moves = self.board.get_available_moves()
        if not moves:
            return False
            
        # Sort by the number of onward moves (fewer options first)
        moves.sort(key=lambda move: len(self.board.get_available_moves_from(move)))
        
        for move_x, move_y in moves:
            if self.board.move(move_x, move_y):
                if self._solve(tour):
                    return True
                self.board.undo_move()
        
        return False

if __name__ == '__main__':
    # Test the knight's tour solver
    knight = Knight(5, 5)
    knight.set_start_position(0, 0)
    
    if knight.solve_closed_tour():
        print("Solution found!")
        knight.board.printBoard()
        knight.board.printMoves()
    else:
        print("No solution exists from the given starting position")