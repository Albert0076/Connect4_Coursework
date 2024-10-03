import numpy as np
from connect4_structure_prototype import Grid, Cell
import random

MAX = 10
MIN = -10

pos_weights = [0, 1, 2, 3, 3, 2, 1 ,0]
# Player 1: 1, Player 2: 2, Empty: 0


def convert_to_np(grid: Grid):
    np_grid = np.zeros((grid.num_columns, grid.num_rows))
    for cell in grid.cells.values():
        if not cell.is_empty():
            if cell.symbol == "r":
                np_grid[cell.column, cell.row] = 1

            else:
                np_grid[cell.column, cell.row] = 2

    return np_grid


def check_win(grid, p_num: int):
    # This function is based of one found on StackOverflow by user 101arrowz Link:
    # https://stackoverflow.com/questions/56351369/easier-way-to-check-for-four-in-row-column-diagonal-in-connect
    # -four-game
    win_num: int = 0
    found = False
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 0:
                break
                # If the connect-4 game is working if there is an empty cell there cannot be any full cells above it,
                # So we can go to the next column

            try:  # Vertical
                if grid[i, j] == grid[i + 1, j] == grid[i + 2, j] == grid[i + 3, j]:
                    # The computer is intended for default rules for now so we only have to worry about checking for 4.
                    found = True
                    win_num = grid[i, j]

            except IndexError:
                pass

            try:  # Horizontal
                if grid[i, j] == grid[i, j + 1] == grid[i, j + 2] == grid[i, j + 3]:
                    found = True
                    win_num = grid[i, j]

            except IndexError:
                pass

            try:  # Diagonal 1
                if grid[i, j] == grid[i + 1, j + 1] == grid[i + 2, j + 2] == grid[i + 3, j + 3]:
                    found = True
                    win_num = grid[i, j]

            except IndexError:
                pass

            try:  # Diagonal 2
                if grid[i, j] == grid[i + 1, j - 1] == grid[i + 2, j - 2] == grid[i + 3, j - 3]:
                    found = True
                    win_num = grid[i, j]

            except IndexError:
                pass

            if found:
                if win_num == p_num:
                    return MAX

                else:
                    return MIN

    return 0


def evaluate(grid, p_num, op_num):
    three_count = 0
    pos_count = 0
    piece_count = 0
    # use the same code as check win just only checking for three in a rows.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == p_num:
                piece_count += 1
                win_change = 1
                pos_count += pos_weights[i]

            elif grid[i, j] == op_num:
                piece_count += 1
                win_change = -1
                pos_count -= pos_weights[i]

            else:
                win_change = 0
            if grid[i, j] == 0:
                break
            try:  # Vertical
                if grid[i, j] == grid[i + 1, j] == grid[i + 2, j]:
                    three_count += win_change

            except IndexError:
                pass

            try:
                if grid[i, j] == grid[i, j + 1] == grid[i, j + 2]:
                    three_count += win_change

            except IndexError:
                pass

            try:
                if grid[i, j] == grid[i + 1, j + 1] == grid[i + 2, j + 2]:
                    three_count += win_change
            except IndexError:
                pass

            try:
                if grid[i, j] == grid[i + 1, j - 1] == grid[i + 2, j - 2]:
                    three_count += win_change

            except IndexError:
                pass

    return_val = 2*three_count + pos_count//piece_count
    if return_val >= MAX:
        return_val = MAX-1
    if return_val <= MIN:
        return_val = MIN+1


    return return_val


def minimax(is_max, grid, alpha, beta, depth, p_num):
    if p_num == 1:
        op_num = 2
    else:
        op_num = 1
    win = check_win(grid, p_num)
    if win != 0:
        return win

    if depth == 0:
        return evaluate(grid, p_num, op_num)

    if is_full(grid):
        return 0

    if is_max:
        best = MIN
        for i in range(grid.shape[0]):
            try:
                val = minimax(False, add_piece(grid, p_num, i), alpha, beta, depth - 1, p_num)
                best = max(best, val)
                alpha = max(best, alpha)
                if beta <= alpha:
                    break

            except IndexError:
                pass

    else:
        best = MAX
        for i in range(grid.shape[0]):
            try:
                val = minimax(True, add_piece(grid, op_num, i), alpha, beta, depth - 1, p_num)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break

            except IndexError:
                pass

    return best


def find_best_move(grid, p_num):
    if p_num == 1:
        player_dict = {True: 1, False: 2}
    else:
        player_dict = {True: 2, False: 1}

    alpha = MIN
    beta = MAX
    best = MIN
    possible_moves = []
    for i in range(grid.shape[0]):
        try:
            val = minimax(False, add_piece(grid, p_num, i), alpha, beta, 8, p_num)
            best = max(best, val)
            alpha = max(best, alpha)
            possible_moves.append(val)
            if beta <= alpha:
                break
        except IndexError:
            possible_moves.append(MIN)

    return possible_moves.index(max(possible_moves))


def add_piece(p_grid, p_num, column):
    new_grid = np.copy(p_grid)
    for i in range(new_grid.shape[1]):
        if new_grid[column, i] == 0:
            new_grid[column, i] = p_num
            return new_grid

    raise IndexError


def is_full(grid):
    for num in grid.flatten():
        if num == 0:
            return False

    return True


if __name__ == "__main__":
    grid = convert_to_np(Grid())
    for i in range(3):
        grid = add_piece(grid, 1, 5)
    print(find_best_move(grid, 1))






# May need a more sophisticated evaluate function in order to make it make better and faster moves
