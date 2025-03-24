import math
from main_project import connect4_grid as structure
import time
import copy

symbols = {False: "B",
           True: "R"}


def minimax(grid: structure.Grid, is_max, depth, alpha=-math.inf, beta=math.inf):
    if grid.grid_full() or depth == 0:
        return 0

    if grid.check_win():
        if is_max:
            return -math.inf

        return math.inf

    if is_max:
        value = -math.inf
        for column in range(grid.num_columns):
            try:
                next_grid = copy.deepcopy(grid)
                next_grid.add_piece(column, symbols[is_max])
                value = max(value, minimax(next_grid, False, depth - 1, alpha, beta))

                if value > beta:
                    break

                alpha = max(alpha, value)

            except IndexError:
                pass

        return value

    value = math.inf

    for column in range(grid.num_columns):
        try:
            next_grid = copy.deepcopy(grid)
            next_grid.add_piece(column, symbols[is_max])
            value = min(value, minimax(next_grid, True, depth - 1, alpha, beta))

            if value < alpha:
                break

            beta = min(value, beta)

        except IndexError:
            pass

    return value


if __name__ == "__main__":
    grid = structure.Grid()
    y_values = []
    for depth in range(1, 7):
        print(depth)
        total = 0
        N = 5
        for i in range(N):
            start_time = time.time()
            minimax(grid, True, depth)
            total += (time.time() - start_time)

        y_values.append(total / N)

    print(y_values)

# This is code is meant to show a basic implementation of the minimax algorithm and is supposed to line up well
# With the pseudocode written.
