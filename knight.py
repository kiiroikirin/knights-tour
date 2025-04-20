"""knights.py
a program to solve an NxM knights tour board
input: starting square
output: sequence of moves
"""

# ideas, parallelise and have knights explore K = ... different boards.

"""phase 1: create a single player playable backend

phase 2: add solving ai with backtracking

phase 3: add front-end

phase 4: increase number of knights traverseering the game-tree parallelly."""


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

    def distance(self, knight):
        return abs(knight.x - self.x) + abs(knight.y - self.y)

    def siren(self, knight):
        """Check if the knight can move to this cell"""
        if self.distance(knight) == 3 and self.visited == False:
            return True 

class Board:
    def __init__(self, rows, cols):
        """create a board of size NxM"""
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.x = 0 # knight's x coordinate
        self.y = 0  # knight's y coordinate
        self.moveCount = 0
    
    def get_cell(self, x, y):
        """Retrieve a specific cell on the board"""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.board[x][y]
        else:
            raise ValueError("Cell coordinates out of bounds")

    def check_move(self, x, y):
        """Check if the knight can move to a specific cell"""
        if self.get_cell(x, y).visited:
            raise ValueError("Cell already visited")
        else:
            # check in bounds:
            if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
                raise ValueError("Cell coordinates out of bounds")
        return True
    
    def get_available_moves(self):
        """Get all available moves for the knight"""
        moves = []
        knight = Knight()
        knight.x = self.x
        knight.y = self.y
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            # check in bounds:
            if self.x + dx < 0 or self.x + dx >= self.rows or self.y + dy < 0 or self.y + dy >= self.cols:
                continue
            new_x = self.x + dx
            new_y = self.y + dy
            if self.get_cell(new_x, new_y).siren(knight):
                moves.append((new_x, new_y))
        return moves

    def printBoard(self):
        """print the board"""
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print(f"Knight position: ({self.x}, {self.y})")
        print(f"Moves available: {len(self.get_available_moves())} and they are {self.get_available_moves()}")
    
    def move(self, x, y):
        """move the knight to a new square"""
        if self.get_cell(x, y).visited:
            raise ValueError("Cell already visited")
        else:
            self.x = x
            self.y = y
            self.moveCount += 1
            self.board[x][y].mark_visited()
            return self.moveCount

class Knight:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.moveCount = 0
        self.board = Board(8, 7)

    def move(self, x, y):
        """move the knight to a new square"""
        self.board.move(x, y)
        self.moveCount += 1
        return self.moveCount

if __name__ == '__main__':
    player = Knight()
    player.board.printBoard()
    for i in range(100):
        print("Knight move")
        moves = player.board.get_available_moves()
        if len(moves) == 0:
            print("No more moves available")
            break
        else:
            x, y = moves[0]
            player.move(x, y)
            player.board.printBoard()
    print("Knight move")

