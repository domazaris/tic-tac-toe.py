#!/usr/bin/env python3
""" Just a fun game of tic tac toe """


def printBoard(board):
    """ Print the game board """
    rows = []
    for row in board:
        rows.append("|".join(row))
    print("\n-+-+-\n".join(rows))

    
def threeInARow(board, player):
    """ Return true if three of a kind are in a row """
    result = False
    for idx in range(3):
        # Check rows
        result |= player == board[idx][0] == board[idx][1] == board[idx][2]

        # Check colums
        result |= player == board[0][idx] == board[1][idx] == board[2][idx]

    result |= player == board[0][0] == board[1][1] == board[2][2]
    result |= player == board[0][2] == board[1][1] == board[2][0]
        
    return result


def fullBoard(board):
    """ Return true if board is full (draw)"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def gameOver(board):
    """ Return true if game over """
    return threeInARow(board, "o") or threeInARow(board, "x") or fullBoard(board)


def gameResult(board):
    """ Print the winner of the game"""
    if threeInARow(board, "o"):
        print("YOU WIN")
    elif threeInARow(board, "x"):
        print("YOU LOSE")
    else:
        print("It's a draw :|")


def newBoard():
    """ Return a blank board """
    return [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]


def userTurn(board):
    """ Get user input, then place """
    while True:
        turn = input("Your move. Place in coords of a position e.g. 0,0: ")
        if turn:
            turn = turn.split(',')
            if len(turn) == 2:
                try:
                    x = int(turn[0])
                    y = int(turn[1])
                    if x >= 0 and x <= 2 and y >=0 and y <= 2:
                        coords = [x, y]
                        if board[x][y] is not " ":
                            print("Space is already taken")
                        else:
                            board[x][y] = "o"
                            return
                    else:
                        print("Invalid input")
                except ValueError:
                    pass

def twoInARow(board):
    """ Check if there is an opportunity to win. If yes, return winning coords """
    coords = None

    # Rows / Columns (rotate for column check
    for x in range(3):
        row = board[x]
        count_x = sum(1 for i in row if i == "x")
        count_o = sum(1 for i in row if i == "o")
        count_n = sum(1 for i in row if i == " ")
        if count_n == 1 and (count_x == 2 or count_o == 2):
            # hit, get the coords
            y = row.index(" ")
            coords = [x, y]

    # Columns - rotate the board
    if not coords:
        rotated_board = list(zip(*board[::-1]))
        for y in range(3):
            row = rotated_board[y]
            count_x = sum(1 for i in row if i == "x")
            count_o = sum(1 for i in row if i == "o")
            count_n = sum(1 for i in row if i == " ")
            if count_n == 1 and (count_x == 2 or count_o == 2):
                # hit, get the coords (invert the row to get accurate coords)
                x = row[::-1].index(" ")
                coords = [x, y]
                    
    # Diagonal: starting top left corner
    if not coords:
        top = board[0][0]
        middle = board[1][1]
        bottom = board[2][2]

        if top is not " " and top == middle:
            # bottom
            coords = [2,2]
        if middle is not " " and middle == bottom:
            # top
            coords = [0,0]
        elif bottom is not " " and top == bottom:
            # middle
            coords = [1,1]

    # Diagonal: tarting top right corner
    if not coords:
        top = board[0][2]
        middle = board[1][1]
        bottom = board[2][0]

        if top is not " " and top == middle:
            # bottom
            coords = [2,0]
        if middle is not " " and middle == bottom:
            # top
            coords = [0,2]
        elif	bottom is not " " and top == bottom:
            # middle
            coords = [1,1]

    # Done
    return coords


def cpuTurn(board):
    """ CPU turn in the game """
    # Win or block: Check for 2 in a row
    coords = twoInARow(board)
    if coords:
        board[coords[0]][coords[1]] = "x"
        return

    # Fork or Block Fork:
    # Center:
    # Opp Corner:
    # Empty Corner:
    # Empty Side: 


def main():
    """ """
    try:
        board = newBoard()
        while not gameOver(board):
            printBoard(board)
            userTurn(board)
            if not gameOver(board):
                cpuTurn(board)

        printBoard(board)
        gameResult(board)
    except KeyboardInterrupt:
        print("\nAlright, quitter....")
    except EOFError:
        print("\nAlright, quitter....")
    

if __name__ == "__main__":
    main()
