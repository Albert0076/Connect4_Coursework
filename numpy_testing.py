import numpy as np
import copy
from connect4_structure_prototype import Grid, Cell
import random

MAX = 100
MIN = -100


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
                    return 10

                else:
                    return -10

    return 0


player_dict = {True: 1, False: 2}


def minimax(alpha, beta, is_max, p_grid, depth):
    # Currently we use the check_win function to evaluate the value of a grid. To make a faster but maybe less
    # accurate computer we could only go to a certain depth but have a more sophisticated evaluate function
    if depth == 0:
        return 0
    p_num = player_dict[is_max]
    win = check_win(p_grid, p_num)
    if win != 0:
        return win

    val_list = []
    if is_max:
        best = MIN

    else:
        best = MAX
    for column in range(p_grid.shape[0]):
        try:
            val_list.append(minimax(alpha, beta, not is_max, add_piece(p_grid, p_num, column), depth - 1))
            if is_max:
                best = max(best, val_list[-1])
                alpha = max(alpha, best)

            else:
                best = min(best, val_list[-1])
                beta = min(beta, best)

            if beta <= alpha:
                break

        except:
            pass

    return best


def find_best_move(grid, p_num, depth):
    if p_num == 1:
        is_max = True

    else:
        is_max = False
    move_values = []
    for i in range(grid.shape[0]):
        try:
            move_values.append(minimax(MIN, MAX, is_max, add_piece(grid, p_num, i), depth))

        except IndexError:
            move_values.append(MIN)
        if move_values[-1] == 10:
            break

    max_val = np.max(move_values)
    max_values = np.where(move_values == max_val)[0]
    return random.choice(max_values)


def add_piece(p_grid, p_num, column):
    new_grid = copy.deepcopy(p_grid) # This copy is using a lot of time may need to get a different system
    for i in range(new_grid.shape[1]):
        if new_grid[column, i] == 0:
            new_grid[column, i] = p_num
            return new_grid

    raise IndexError

def play_game():
    grid = convert_to_np(Grid())
    while check_win(grid, 1) == 0:
        move = find_best_move(grid, 1, 9)
        print(move)
        grid = add_piece(grid, 1, move)
        print(grid)
        move = int(input())
        grid = add_piece(grid, 2, move)



if __name__ == "__main__":
    play_game()
