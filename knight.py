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
        self.board[self.x][self.y].mark_visited()
        self.moves = []
    
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

    def get_available_moves_from(self, cell):
        """Get all available moves from a specific cell"""
        moves = []
        knight = Knight()
        knight.x = cell[0]
        knight.y = cell[1]
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            # check in bounds:
            if cell[0] + dx < 0 or cell[0] + dx >= self.rows or cell[1] + dy < 0 or cell[1] + dy >= self.cols:
                continue
            new_x = cell[0] + dx
            new_y = cell[1] + dy
            if self.get_cell(new_x, new_y).siren(knight):
                moves.append((new_x, new_y))

        return moves

    def printBoard(self):
        """print the board"""
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print(f"Knight position: ({self.x}, {self.y})")
        print(f"Moves available: {len(self.get_available_moves())} and they are {self.get_available_moves()}")
    
    def isSolved(self):
        """check if the board is solved"""
        for row in self.board:
            for cell in row:
                if not cell.visited:
                    return False
        return True
    
    def undo_move(self, x, y):
        """undo the knight's last move"""
        if self.get_cell(x, y).visited:
            self.x = x
            self.y = y
            self.moveCount -= 1
            self.board[x][y].visited = False
            self.moves.pop()
            return self.moveCount
        else:
            raise ValueError("Cell not visited")

    def move(self, x, y):
        """move the knight to a new square"""
        if self.get_cell(x, y).visited:
            raise ValueError("Cell already visited")
        else:
            self.x = x
            self.y = y
            self.moveCount += 1
            self.board[x][y].mark_visited()
            self.moves.append((x, y))
            return self.moveCount

    def printMoves(self):
        """print the moves made by the knight"""
        print("Moves made:")
        print(self.moves)
        print(f"Total moves: {self.moveCount}")

class Knight:
    def __init__(self, N=8, M=7):
        self.x = 0
        self.y = 0
        self.moveCount = 0
        self.board = Board(N, M)

    def move(self, x, y):
        """move the knight to a new square"""
        self.board.move(x, y)
        self.moveCount += 1
        return self.moveCount

    def encode_board(self):
        """encodes the board so rotations and reflections are the same"""
        board_as_str = "".join("1" if cell.visited else "0" for row in self.board.board for cell in row)
        print(board_as_str)
        return int(board_as_str,2)
        

    def solve(self):
        if self.board.isSolved():
            return True
        # warnsdorf heuristic: sort the moves by the number of available moves from that square
        moves = sorted(self.board.get_available_moves(), key=lambda move: len(self.board.get_available_moves_from(move)))
        for move in moves:
            self.board.move(*move)
            if self.solve():
                return True
            self.board.undo_move(*move)
        return False

    def memory_solve(self, visited=None):
        """solve the knights tour problem with recursive dfs and orientation memory savings"""

        if visited is None:
            visited = set()

        board_state = self.encode_board()
        if board_state in visited:
            return False
        visited.add(board_state)

        if self.board.isSolved():
            return True
        for move in self.board.get_available_moves():
            self.board.move(*move)
            if self.solve():
                return True
            self.board.undo_move(*move)

        visited.remove(board_state)
        return False



if __name__ == '__main__':
    player = Knight(7,8)
    player.board.printBoard()
    player.solve()
    player.board.printBoard()
    player.board.printMoves()
    player = Knight(8,8)
    player.board.printBoard()
    player.solve()
    player.board.printBoard()
    player.board.printMoves()
    player = Knight(10,8)
    player.board.printBoard()
    player.solve()
    player.board.printBoard()
    player.board.printMoves()

