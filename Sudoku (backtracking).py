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

"""
1. pick an empty square
2. try each numbers
3. find one that works
4. repeat until finding invalid value
5. backtrack (main algorithm)
"""

# print out the board
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])

            else:
                print(str(board[i][j]) + " ", end = "")

# 1. find an empty square
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None
            

# 2. check if the number is valid
def is_valid(board, num, position):

    # check row
    for i in range(len(board[0])):
        if board[position[0]][i] == num and position[1] != i:
            return False
        
    # check column
    for i in range(len(board)):
        if board[i][position[1]] == num and position[0] != i:
            return False
        
    # check box
    # find the 3 x 3 box it's in
    col = position[1] // 3
    row = position[0] // 3

    # loop through the box
    for i in range(row*3, row*3 + 3):
        for j in range(col*3, col*3 + 3):
            if board[i][j] == num and position != (i, j):
                return False
            
    return True

# backtracking
def solve(board):
    find = find_empty(board)

    # the end the of the board
    if not find:
        return True
    
    row, col = find

    for i in range(1,10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

print_board(board)
solve(board)
print("")
print_board(board)
