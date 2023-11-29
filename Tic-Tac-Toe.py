# student name: Ray Cho
# student number: 74320474

# A command-line Tic-Tac-Toe game 
import random

board = [' '] * 9 # A list of 9 strings, one for each cell, 
                  # will contain ' ' or 'X' or 'O'
played = set()   # A set to keep track of the played cells 


def init() -> None:
    """ prints the banner messages 
        and prints the intial board on the screen
    """
    first_move = random.choice(['X', 'O'])
    print("Welcome to Tic-Tac-Toe!")
    if first_move == 'X':
        print("You play X (first move) and computer plays O.")
    else:
        played.add('comp first')
        print("You play X and computer plays O (first move).")

    print("Computer plays strategically.")
    printBoard()

def printBoard() -> None:
    """ prints the board on the screen based on the values in the board list """
    print("\n")
    for i in range(9):
        if i % 3 == 0:
            if i != 0:
                print("\n   --+---+--    --+---+--")
            print("  ", end=" ")
        if i % 3 == 2:
            print(f"{board[i]}", end=" ")
            print(f"   {i-2} | {i-1} | {i}", end=" ")
        else:
            print(f"{board[i]} |", end=" ")
    print("\n")


def playerNextMove() -> None:
    """ prompts the player for a valid cell number, 
        and prints the info and the updated board;
        error checks that the input is a valid cell number 
    """
    if 'comp first' in played:
        played.remove('comp first')
        return None 
    player_nextmove = input("Next move for X (state a valid cell num): ")
    
    # check if input is numeric and between 0 and 8 and not in the played cells
    while not player_nextmove.isnumeric() or int(player_nextmove) > 8 or int(player_nextmove) < 0 or int(player_nextmove) in played:
        if not player_nextmove.isnumeric():
            print("Must be an integer")
            player_nextmove = input("Next move for X (state a valid cell num): ")
        else:
            print("Must be an valid cell number")
            player_nextmove = input("Next move for X (state a valid cell num): ")
    player_nextmove_int = int(player_nextmove)

    # update the board and the played cell set
    played.add(player_nextmove_int)
    board[player_nextmove_int] = 'X'
    print(f"You chose cell {player_nextmove_int}")
    printBoard()

def computerNextMove() -> None:
    """ Computer strategically chooses a valid cell, 
        and prints the info and the updated board 
    """
    
    # a function is used to determine the next move after returning a value
    def nextmove():

        # helper function that finds an available corner 
        def place_corner():
            return random.choice([x for x in [0,2,6,8] if x not in played])
            
        # helper function that finds an available edge 
        def place_edge():
            return random.choice([x for x in [1,3,5,7] if x not in played])
        
        # check if the computer can win in the next move by traversing through the board
        for i in range(9):
            if i not in played:
                board[i] = 'O'
                if hasWon('O'):
                    return i
                else:
                    board[i] = ' '

        # check if the player is about to win and block it
        for i in range(9):
            if i not in played:
                board[i] = 'X'
                if hasWon('X'):
                    return i
                else:
                    board[i] = ' '

        # if the computer makes the first move
        # --------------------------------------

        # place it in a corner on the first move 
        if len(played) == 0:
            return random.choice([0, 2, 6, 8])
        
        # if the computer makes the first move in the corner and the player place 'X' in the center
        # place 'O' in the opposite corner
        if len(played) == 2 and board[4] == 'X':
            comp_first_move = board.index('O')
            match comp_first_move:
                case 0: return 8
                case 2: return 6
                case 6: return 2
                case 8: return 0
        
        # if the computer makes the first move in the corner and the player place 'X' not in the center
        # if 'X' is placed adjacent to 'O', avoid O X O 
        # otherwise, place the second 'O' in any unoccupied corner

        # helper function to check if O X O occurs on the four sides
        # only have to check the sides since 'O' is in a corner
        def comp_o_x_o(temp):
            # add the undetermined move to played cells
            played.add(temp)
            # check if O X O is on a side
            if all(x in played for x in [0,1,2]) or all(x in played for x in [0,3,6]) or all(x in played for x in [2,5,8]) or all(x in played for x in [6,7,8]):
                return True
            # if it's not then remove it from played cells
            played.remove(temp)
            return False

        if len(played) == 2 and board[4] != 'X':
            comp_second_move = place_corner()
            # we need the undetermined move later so we store it in a helper variable temp 
            temp = comp_second_move
            if comp_o_x_o(temp):
                # new move that avoids O X O
                comp_second_move = place_corner()
                # remove the wrong move
                played.remove(temp)
                return comp_second_move
            return comp_second_move

        # --------------------------------------
        # end of computer making the first move

        # if the player makes the first move
        # --------------------------------------
        

        # if the player's first move is in a corner
        # place 'O' in the center
        if len(played) == 1 and (board[0] == 'X' or board[2] == 'X' or board[6] == 'X' or board[8] == 'X'):
            played.add('corner') # for the next move to identify the first move is in the corner
            return 4 
        
        # if the player's first move is in a corner
        # the second 'O' should be on an edge
        if 'corner' in played:
            played.remove('corner') # 'corner' is not needed in further moves
            return place_edge()
        
        # if the player's first move is in the center
        # place 'O' in a corner
        if len(played) == 1 and board[4] == 'X':
            return place_corner()

        # if the player's first move is on an edge
        # place 'O' in the center
        if len(played) == 1 and (board[1] == 'X' or board[3] == 'X' or board[5] == 'X' or board[7] == 'X'):
            return 4
        
        # --------------------------------------
        # end of the player making the first move
        
        # in any other scenarios, place 'O' in a corner
        
        return place_corner()
        

    # update the board and the played cell set
    comp_nextmove = nextmove()
    played.add(comp_nextmove)
    board[comp_nextmove] = 'O'
    print(f"Computuer chose cell {comp_nextmove}")
    printBoard()


def hasWon(who: str) -> bool:
    """ returns True if who (being passed 'X' or 'O') has won, False otherwise """
    for i in range(3):
        # vertical line
        if who == board[i] == board[i+3] == board[i+6]:
            return True
        
        # horizontal line
        if who == board[i*3] == board[i*3+1] == board[i*3+2]:
            return True
        
    # top left to bot right diagonal 
    if who == board[0] == board[4] == board[8]:
        return True
    
    # top right to bot left diagonal 
    if who == board[2] == board[4] == board[6]:
        return True
        
    return False

def terminate(who: str) -> bool:
    """ returns True if who (being passed 'X' or 'O') has won or if it's a draw, False otherwise;
        it also prints the final messages:
                "You won! Thanks for playing." or 
                "You lost! Thanks for playing." or 
                "A draw! Thanks for playing."  
    """
    if who == 'X' and hasWon(who):
        print("You won! Thanks for playing.")
        return True
    if who == 'O' and hasWon(who):
        print("You lost! Thanks for playing.")
        return True
    if len(played) == 9:
        print("A draw! Thanks for playing." )
        return True
    return False

if __name__ == "__main__":
    # Use as is. 
    init()
    while True:
        playerNextMove()            # X starts first
        if(terminate('X')): break   # if X won or a draw, print message and terminate
        computerNextMove()          # computer plays O
        if(terminate('O')): break   # if O won or a draw, print message and terminate
            
