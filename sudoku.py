sudoku_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
] # made a list of lists to represent a sudoku puzzle. the 0's indicate an empty cell that at some point will be solved with a solver function
# this puzzle will be used as a test case to demonstrate and validate the coming algorithms

def is_valid(puzzle, row, col, num): # this function will do exactly what it says. It will check if a number is valid in a given cell
    if num in puzzle[row]:
        return False # if the number exists in the row, then false is returned and the function exits immediately

    for i in range(9):
        if puzzle[i][col] == num: # accesses the cell in the column at each row i and compares it with num
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3) # this will check for the sub 3x3 grids. multiplying by 3 will give the starting row and column for that subgrid
    for i in range(start_row, start_row + 3): # iterates through the rows of the subgrid
        for j in range(start_col, start_col + 3): # iterates through the columns
            if puzzle[i][j] == num:
                return False

    return True

def find_empty_location(puzzle): # this functon will be used to find the next empty cell with the fewest possible options
    min_options = 10 # this is more than the maximum possible options which is 9
    min_cell = None
    found_empty_cell = False

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                found_empty_cell = True
                options = 0 # so an empty cell has been found and now we initialize a counter to track the number of valid numbers that can go into this empty cell
                for num in range(1, 10):
                    if is_valid(puzzle, row, col, num):
                        options += 1
                if options == 0: # there are no valid options for this cell and the puzzle is unsolvable
                    return (-1, -1) # a special marker to signal that its unsolvable
                if options < min_options:
                    min_options = options
                    min_cell = (row, col)
                    if min_options == 1:
                        return min_cell  # it's the best candidate and it cant get better than this

    if not found_empty_cell:
        return None  # this means puzzle is solved
    elif min_cell is None: # there are empty cells but no valid options so puzzle is unsolvable and we return that special marker
        return (-1, -1)
    else:
        return min_cell

# learned a bit about combining backtracking with the MCV heurstic which are 2 things ive never learned before but learned through coding this program and trying to make it
# as efficient as possible. Backtracking with the MCV heuristic means solving a problem incrementally by exploring possible solutions while at the same time, prioritizing the
# most constrained option to reduce the likelihood of invalid paths and excessive backtracking. The following function will do this by using find_empty_location to select
# the cell with the fewest valid numbers and recursively trying valid placements while backtracking when needed
def solve_sudoku(puzzle):
    empty_cell = find_empty_location(puzzle) # calls helper function find_empty_location to find the next empty cell
    if empty_cell is None:
        return True

    row, col = empty_cell # row will represent the row index of the empty cell and column will represent the column index of the empty cell

    for num in range(1, 10):
        if is_valid(puzzle, row, col, num): # checks if placing the num in the (row, col) position is allowed
            puzzle[row][col] = num  # places the number temporarily. if this placement ends up being invalid later, it'll be undone during backtracking
            if solve_sudoku(puzzle):  # recursion call. learned this in my last cs class
                return True
            puzzle[row][col] = 0  # this will undo that temporary placement if the recursion call on solve_sudoku returns false
    return False

# this displays the puzzle in a formatted way. the function will iterate through each row and format the cells for better readability
def print_sudoku(puzzle):
    for row in puzzle:
        print(" ".join(str(num) if num != 0 else "." for num in row)) # formats each row to replace 0 with "." for better readability, joins the numbers with a space
        # for neat display
    print()

# example puzzle for testing. its a simple puzzle.
easy_puzzle = [
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


print("Original Sudoku Puzzle:")
print_sudoku(easy_puzzle)

if solve_sudoku(easy_puzzle): # this just checks if the solver successfully solved the puzzle
    print("Solved Sudoku Puzzle:")
    print_sudoku(easy_puzzle)
else:
    print("No solution exists for the given puzzle.") # message if the solver determines that the puzzle cant be solved