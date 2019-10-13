#!/usr/bin/env python3
""" Just a fun game of tic tac toe """

import random
import sys


def print_board(board):
    """ Print the game board """
    rows = []
    for row in board:
        rows.append("|".join(row))
    print("\n-+-+-\n".join(rows))


def three_in_a_row(board, player):
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


def full_board(board):
    """ Return true if board is full (draw)"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def game_over(board):
    """ Return true if game over """
    return three_in_a_row(board, "o") or three_in_a_row(board, "x") or full_board(board)


def game_result(board):
    """ Print the winner of the game"""
    if three_in_a_row(board, "o"):
        print("YOU WIN")
    elif three_in_a_row(board, "x"):
        print("YOU LOSE")
    else:
        print("It's a draw :|")


def new_board():
    """ Return a blank board """
    return [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]


def user_turn(board):
    """ Get user input, then place """
    print_board(board)
    while True:
        turn = input("Your move. Place in coords of a position e.g. 0,0: ")
        if turn:
            turn = turn.split(',')
            if len(turn) == 2:
                try:
                    x = int(turn[0])
                    y = int(turn[1])
                    if x >= 0 and x <= 2 and y >= 0 and y <= 2:
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


def get_column(board, col):
    """ Return a list of the column at the given index """
    column = []
    for row in board:
        column.append(row[col])
    return column


def two_in_a_row(board):
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
            column = get_column(board, y)
            count_x = sum(1 for i in column if i == "x")
            count_o = sum(1 for i in column if i == "o")
            count_n = sum(1 for i in column if i == " ")
            if count_n == 1 and (count_x == 2 or count_o == 2):
                # hit, get the coords (invert the row to get accurate coords)
                x = column.index(" ")
                coords = [x, y]

    # Diagonal: starting top left corner
    if not coords:
        top = board[0][0]
        middle = board[1][1]
        bottom = board[2][2]

        if bottom is " " and top is not " " and top == middle:
            # bottom
            coords = [2, 2]
        elif top is " " and middle is not " " and middle == bottom:
            # top
            coords = [0, 0]
        elif middle is " " and bottom is not " " and top == bottom:
            # middle
            coords = [1, 1]
            print(coords)

    # Diagonal: tarting top right corner
    if not coords:
        top = board[0][2]
        middle = board[1][1]
        bottom = board[2][0]

        if bottom is " " and top is not " " and top == middle:
            # bottom
            coords = [2, 0]
        elif top is " " and middle is not " " and middle == bottom:
            # top
            coords = [0, 2]
        elif middle is " " and bottom is not " " and top == bottom:
            # middle
            coords = [1, 1]

    # Done
    return coords


def is_corner(x, y):
    """ Return true if corner """
    return x != 1 and y != 1


def get_diagonal(board, row, col):
    """ Return a list of a diagonal row, starting from the given coords """
    if [row, col] == [0, 0] or [row, col] == [2, 2]:
        return [board[0][0], board[1][1], board[2][2]]
    elif [row, col] == [0, 2] or [row, col] == [2, 0]:
        return [board[0][2], board[1][1], board[2][0]]


def find_fork(board):
    """ Return the locations of a potential fork (or None) """
    for row in range(3):
        for col in range(3):
            x_fork_count = 0
            o_fork_count = 0
            cell = board[row][col]

            if cell == " ":
                axes = [board[row], get_column(board, col)]
                if is_corner(row, col):
                    axes.append(get_diagonal(board, row, col))

                # Check for forks in row, col and diagonal
                for axis in axes:
                    # Check axis
                    count_x = sum(1 for i in axis if i == "x")
                    count_o = sum(1 for i in axis if i == "o")
                    count_n = sum(1 for i in axis if i == " ")
                    if count_n == 2 and count_o == 1:
                        o_fork_count += 1
                    if count_n == 2 and count_x == 1:
                        x_fork_count += 1

                if x_fork_count >= 2 or o_fork_count >= 2:
                    return [row, col]

    return None


def find_empty_middle(board):
    """ Returns middle coords if empty """
    if board[1][1] == " ":
        return [1, 1]
    else:
        return None


def find_opposite_corner(board):
    """ Returns coordinates if there is a blank opposite corner """
    if board[0][0] == "o" and board[2][2] == " ":
        return [2, 2]
    elif board[0][2] == "o" and board[2][0] == " ":
        return [2, 0]
    elif board[2][0] == "o" and board[0][2] == " ":
        return [0, 2]
    elif board[2][2] == "o" and board[0][0] == " ":
        return [0, 0]
    else:
        return None


def find_empty_corner(board):
    """ Return coords of first empty corner """
    if board[0][0] == " ":
        return [0, 0]
    elif board[0][2] == " ":
        return [0, 2]
    elif board[2][0] == " ":
        return [2, 0]
    elif board[2][2] == " ":
        return [2, 2]
    else:
        return None


def find_empty_side(board):
    """ Return coords of first found empty side """
    if board[0][1] == " ":
        return [0, 1]
    elif board[1][0] == " ":
        return [1, 0]
    elif board[1][2] == " ":
        return [1, 2]
    elif board[2][1] == " ":
        return [2, 1]
    else:
        return None


def cpu_turn(board):
    """ CPU turn in the game """
    moves = [two_in_a_row, find_fork, find_empty_middle,
             find_opposite_corner, find_empty_corner, find_empty_side]

    for move in moves:
        coords = move(board)
        if coords:
            board[coords[0]][coords[1]] = "x"
            return

    # If we get here, something went wrong
    print("Uh-oh, the game broke! I refuse to lose this")
    sys.exit(0)


def main():
    """ Main function """
    try:
        board = new_board()
        players = [user_turn, cpu_turn]
        random.shuffle(players)

        while not game_over(board):
            players[0](board)
            if not game_over(board):
                players[1](board)

        print_board(board)
        game_result(board)
    except KeyboardInterrupt:
        print("\nAlright, quitter....")
    except EOFError:
        print("\nAlright, quitter....")


if __name__ == "__main__":
    main()