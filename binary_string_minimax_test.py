# A lot of the work on this file is taken from this article:
# https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
# A lot of the minimax code is base on code from: https://github.com/aimacode/aima-python/blob/master/games.py

from connect4_structure_prototype import Grid
import numpy as np
from collections import defaultdict
import time
from random import randint

cache = defaultdict(lambda: None) # cache may not be working properly because it doesn't account for whose turn it is
FULL_GRID = 558517276622718


# The Grid will be represented by an 7x7 grid with the top row being always empty, it will be represented by 8 8bit binary numbers with each byte representing a column

def get_bit_mask(grid: Grid, player):
    position, mask = '', ''
    for column in range(7):
        # We add an extra row at the top to store the board as 2 64-bit binary numbers
        mask += '0'
        position += '0'

        for row in range(5, -1, -1):
            mask += ['0', '1'][not grid.cells[(row, column)].is_empty()]
            position += ['0', '1'][grid.cells[(row, column)].symbol == player]

    return int(position, 2), int(mask, 2)


def print_grid(grid_int):
    grid_str = format(grid_int, '049b')
    output_list = [[" " for j in range(7)] for i in range(7)]
    i, j = 6, 0
    for symbol in grid_str:
        i = (i + 1) % 7
        output_list[i][j] = symbol
        if i == 6:
            j += 1

    str_list_1 = ["".join(column_list) + "\n" for column_list in output_list]
    return "".join(str_list_1)


def check_four_in_a_row(position):
    # Check Horizontal:
    # & - Bitwise And, | - Bitwise Or, ^ - Bitwise XOR, >> - shift bits to the left
    shift = position & (position >> 7)
    if shift & (shift >> 14):
        return True

    # Diagonal \
    shift = position & (position >> 6)
    if shift & (shift >> 12):
        return True

    # Diagonal /
    shift = position & (position >> 8)
    if shift & (shift >> 16):
        return True

    # Vertical
    shift = position & (position >> 1)
    if shift & (shift >> 2):
        return True

    return False


def is_invalid_board(mask):
    return any([mask & (1 << ((7 * i) - 1)) for i in range(1, 8)])


def make_move(position, mask, column):
    new_position = position ^ mask  # The new position will be the opponent's position which we get from doing an XOR
    # mask + (1 << (column*7)) will give an empty grid with 1 piece in the column, adding this to the mask will carry the bit until it is at the top of the column
    new_mask = mask | (mask + (1 << ((6 - column) * 7)))
    return new_position, new_mask


def minimax_alpha_beta(position, mask, is_max, alpha=-np.inf, beta=np.inf):
    """Given a state will calculate the best possible move"""
    # Checks to see if the grid contains a win for the current player:
    if check_four_in_a_row(position ^ mask):
        if is_max:
            return -np.inf

        else:
            return np.inf

    # Checks to see if grid is full
    if mask == FULL_GRID:
        return 0

    next_states = [make_move(position, mask, column) for column in range(7)]
    next_states = [state for state in next_states if (not is_invalid_board(state[1]))]

    if is_max:
        best = -np.inf

    else:
        best = np.inf

    for state in next_states:
        if not cache[(state[0], state[1])] is None:
            val = cache[(state[0], state[1])]
        else:
            val = minimax_alpha_beta(state[0], state[1], not is_max, alpha, beta)
            cache[(state[0], state[1])] = val

        if is_max:
            best = max(best, val)
            alpha = max(best, alpha)
            if beta <= alpha:
                return alpha


        else:
            best = min(best, val)
            beta = min(beta, val)
            if beta <= alpha:
                return beta

    return best


def find_best_move(position, mask):
    values = []
    for i in range(7):
        state = make_move(position, mask, i)
        if is_invalid_board(state[1]):
            values.append(None)  # None is for an illegal move that cannot be made

        else:
            values.append(minimax_alpha_beta(state[0], state[1], False))

    return values


def generate_random_grid(n):
    grid = Grid()
    grid_made = False
    while not grid_made:
        for i in range(n):
            move_made = False
            if i%2 == 0:
                symbol = "R"

            else:
                symbol = "B"

            while not move_made:
                try:
                    grid.add_piece(randint(0, 7), symbol)
                    move_made = True

                except IndexError:
                    pass

        grid_made = not grid.check_win()

    return grid





if __name__ == "__main__":
    grid_0 = Grid()
    for i in range(3):
        grid_0.add_piece(0, "Y")

    grid_0 = get_bit_mask(grid_0, "Y")

    # Starting player wins, optimal move is 4
    test_board_position = int("0000010000101000000110010101000011000110100000001", 2)
    test_board_mask = int("0000111001111100001110111111000111101111110000001", 2)
    print(print_grid(test_board_position))
    print(print_grid(test_board_mask))
    print(minimax_alpha_beta(test_board_position, test_board_mask, True))
    print(find_best_move(test_board_position, test_board_mask))
    # Code seems to be working as it correctly identifies red's winning move.





