import numpy as np
from connect4_structure_prototype import Grid, Cell


# Player 1: 1, Player 2: 2, Empty: 0


def convert_to_np(grid: Grid):
    np_grid = np.zeros((grid.num_rows, grid.num_columns))
    for cell in grid.cells.items():
        if cell.symbol[0] == "r":
            np_grid[cell.row, cell.column] = 1

        elif not cell.is_empty():
            np_grid[cell.row, cell.column] = 2

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
