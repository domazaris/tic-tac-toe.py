#!/usr/bin/env python3


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
        result |= board[idx][0] == board[idx][1] == board[idx][2] == player

        # Check colums
        result |= board[0][idx] == board[1][idx] == board[2][idx] == player

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

def cpuTurn(board):
    """ CPU turn in the game """
    return
    
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
    

if __name__ == "__main__":
    main()
