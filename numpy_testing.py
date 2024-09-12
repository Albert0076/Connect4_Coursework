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
