import numpy as np
from connect4_structure_prototype import Grid, Cell
from scipy import signal

MAX = 10
MIN = -10

pos_weights = [0, 1, 2, 3, 3, 2, 1, 0]


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


def get_kernels(size):
    kernel_h = np.array([[1 for i in range(size)]])
    kernel_v = np.array([[1] for i in range(size)])
    kernel_d1 = np.array([[1 if i == j else 0 for j in range(size)] for i in range(size)])
    kernel_d2 = np.array([[1 if size - i == j + 1 else 0 for j in range(size)] for i in range(size)])
    return kernel_h, kernel_v, kernel_d1, kernel_d2


kernel_3 = get_kernels(3)
kernel_4 = get_kernels(4)


def check_win_fft(grid, p_num, op_num):
    p_num_grid = np.copy(grid)
    op_num_grid = np.copy(grid)
    p_num_grid[p_num_grid != p_num] = 0
    p_num_grid[p_num_grid == p_num] = 1
    op_num_grid[op_num_grid != op_num] = 0
    op_num_grid[op_num_grid == op_num] = 1
    for i in range(4):
        if 4.0 in signal.fftconvolve(p_num_grid, kernel_4[i]):
            return 10

        if 4.0 in signal.fftconvolve(op_num_grid, kernel_4[i]):
            return -10
    return 0


def check_win_2d_conv(grid, p_num, op_num):
    p_num_grid = np.copy(grid)
    op_num_grid = np.copy(grid)
    p_num_grid[p_num_grid != p_num] = 0
    p_num_grid[p_num_grid == p_num] = 1
    op_num_grid[op_num_grid != op_num] = 0
    op_num_grid[op_num_grid == op_num] = 1
    for i in range(4):
        if 4 in signal.convolve2d(p_num_grid, kernel_4[i]):
            return 10

        if 4 in signal.convolve2d(op_num_grid, kernel_4[i]):
            return -10


def check_win(grid, p_num):
    win_num = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                if grid[i, j] == p_num:
                    win_num = MAX

                else:
                    win_num = MIN
                try:
                    if grid[i, j] == grid[i, j + 1] == grid[i, j + 2] == grid[i, j + 3]:
                        return win_num

                except IndexError:
                    pass

                try:
                    if grid[i, j] == grid[i + 1, j] == grid[i + 2, j] == grid[i + 3, j]:
                        return win_num

                except IndexError:
                    pass

                try:
                    if grid[i, j] == grid[i + 1, j + 1] == grid[i + 2, j + 2] == grid[i + 3, j + 3]:
                        return win_num

                except IndexError:
                    pass

                try:
                    if grid[i, j] == grid[i - 1, j + 1] == grid[i - 2, j + 2] == grid[i - 3, j + 3]:
                        return win_num

                except IndexError:
                    pass
    return 0


def evaluate(grid, p_num, op_num):
    p_num_grid = np.copy(grid)
    op_num_grid = np.copy(grid)
    p_num_grid[p_num_grid != p_num] = 0
    p_num_grid[p_num_grid == p_num] = 1
    op_num_grid[op_num_grid != op_num] = 0
    op_num_grid[op_num_grid == op_num] = 1
    three_count = 0
    pos_array = np.array([[1], [1], [1], [4], [3], [2], [1]])
    p_pos = np.dot(pos_array, np.matmul(p_num_grid, np.matrix([[1] for i in range(6)]))]
    op_pos =
    for kernel in kernel_3:
        three_count += np.sum(signal.convolve2d(p_num_grid, kernel) == 3)
        three_count -= np.sum(signal.convolve2d(op_num_grid, kernel) == 3)

    return_val = 2 * three_count
    if return_val >= MAX:
        return_val = MAX - 1
    if return_val <= MIN:
        return_val = MIN + 1

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
    alpha = MIN
    beta = MAX
    best = MIN
    possible_moves = []
    for i in range(grid.shape[0]):
        try:
            val = minimax(False, add_piece(grid, p_num, i), alpha, beta, 6, p_num)
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


# May need a more sophisticated evaluate function in order to make it make better and faster moves