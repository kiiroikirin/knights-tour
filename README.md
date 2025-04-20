this is a quick backtracking solution to the knights-touring problem on an 8x8 board.

I shall be using Python 3.12.7 for the project.

# instructions 

to run simply use `knight-claude-gui-green.py`. this uses a frontend using the `tkinter` library that is sitting on top of my `knight.py` backend.

currently `knight.py` uses a recursive dfs implementation with the Warnsdorff's heuristic. the code uses oop with classes of `Knight`, `Board` and `Cell`.

# features 

- solves NxM board
- solves closed and non-closed tours
- single player mode
- labelled grid
- arbitrary start positions

# future work

implement neural networks solution