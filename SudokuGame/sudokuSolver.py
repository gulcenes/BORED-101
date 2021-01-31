import numpy as np

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]


def possible(board, row, col, val):  # y row , x cols
    # Check rows
    if val in board[row]:  
        return False
    # Check cols
    for r in range(9):  
        if board[r][col] == val:
            return False

    # Check Squares
    sqy = (row // 3) * 3  
    sqx = (col // 3) * 3  

    for r in range(sqy, sqy + 3):  
        for c in range(sqx, sqx + 3):
            if board[r][c] == val:
                return False
    return True


def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c

    return None


def solve(board):
    empty_cell = find_empty(board)

    if not empty_cell:
        return True
    else:
        row, col = empty_cell

    for i in range(1, 10):
        if possible(board, row, col, i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

solve(board)
print(np.matrix(board))