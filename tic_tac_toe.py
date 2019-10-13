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


def get_user_input():
    """ Returns user input or None for invalid input """
    turn = input("Your move. Place in coords of a position e.g. 0,0: ")
    if turn:
        turn = turn.split(',')
        if len(turn) == 2:
            try:
                return [int(turn[0]), int(turn[1])]
            except ValueError:
                pass
    return None


def user_turn(board):
    """ Get user input, then place """
    print_board(board)
    while True:
        coords = get_user_input()
        if coords:
            row = coords[0]
            col = coords[1]
            if 2 >= row >= 0 and 2 >= col >= 0:
                if board[row][col] != " ":
                    print("Space is already taken")
                else:
                    board[row][col] = "o"
                    return
            else:
                print("Invalid input")


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
    for row_idx in range(3):
        row = board[row_idx]
        count_x = sum(1 for i in row if i == "x")
        count_o = sum(1 for i in row if i == "o")
        count_n = sum(1 for i in row if i == " ")
        if count_n == 1 and (count_x == 2 or count_o == 2):
            # hit, get the coords
            col_idx = row.index(" ")
            coords = [row_idx, col_idx]

    # Columns
    if not coords:
        for col_idx in range(3):
            column = get_column(board, col_idx)
            count_x = sum(1 for i in column if i == "x")
            count_o = sum(1 for i in column if i == "o")
            count_n = sum(1 for i in column if i == " ")
            if count_n == 1 and (count_x == 2 or count_o == 2):
                # hit, get the coords (invert the row to get accurate coords)
                row_idx = column.index(" ")
                coords = [row_idx, col_idx]

    # Diagonals
    tops = [[0, 0], [0, 2]]
    for top in tops:
        if not coords:
            diagonal = get_diagonal(board, top[0], top[1])
            top = diagonal[0]
            middle = diagonal[1]
            bottom = diagonal[2]

            if bottom == " " and top != " " and top == middle:
                coords = [2, 2] if top == [0, 0] else [2, 0]
            elif top == " " and middle != " " and middle == bottom:
                coords = [0, 0]	if top == [0, 0] else [0, 2]
            elif middle == " " and bottom != " " and top == bottom:
                coords = [1, 1]

    # Done
    return coords


def is_corner(row, col):
    """ Return true if corner """
    return row != 1 and col != 1


def get_diagonal(board, row, col):
    """ Return a list of a diagonal row, starting from the given coords """
    if [row, col] == [0, 0] or [row, col] == [2, 2]:
        return [board[0][0], board[1][1], board[2][2]]
    if [row, col] == [0, 2] or [row, col] == [2, 0]:
        return [board[0][2], board[1][1], board[2][0]]
    return None


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
    return None


def find_opposite_corner(board):
    """ Returns coordinates if there is a blank opposite corner """
    if board[0][0] == "o" and board[2][2] == " ":
        return [2, 2]
    if board[0][2] == "o" and board[2][0] == " ":
        return [2, 0]
    if board[2][0] == "o" and board[0][2] == " ":
        return [0, 2]
    if board[2][2] == "o" and board[0][0] == " ":
        return [0, 0]
    return None


def find_empty_corner(board):
    """ Return coords of first empty corner """
    if board[0][0] == " ":
        return [0, 0]
    if board[0][2] == " ":
        return [0, 2]
    if board[2][0] == " ":
        return [2, 0]
    if board[2][2] == " ":
        return [2, 2]
    return None


def find_empty_side(board):
    """ Return coords of first found empty side """
    if board[0][1] == " ":
        return [0, 1]
    if board[1][0] == " ":
        return [1, 0]
    if board[1][2] == " ":
        return [1, 2]
    if board[2][1] == " ":
        return [2, 1]
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
