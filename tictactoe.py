import time
import random


class Grid:
    def __init__(self):
        self.array = [[Symbol() for _ in range(3)] for _ in range(3)]

    def add_piece(self, column, row, symbol):
        if self.is_full():
            raise IndexError("Grid is Full")

        self.array[column][row].set_symbol(symbol)

    def check_win(self):
        for i in range(3):
            if self.array[0][i] == self.array[1][i] == self.array[2][i]:
                return True, self.array[0][i].symbol

            if self.array[i][0] == self.array[i][1] == self.array[i][2]:
                return True, self.array[i][0].symbol

        if self.array[0][0] == self.array[1][1] == self.array[2][2]:
            return True, self.array[0][0].symbol

        if self.array[2][0] == self.array[1][1] == self.array[0][2]:
            return True, self.array[1][1].symbol

        return False, None

    def is_full(self):
        for column in self.array:
            for piece in column:
                if piece.is_empty():
                    return False

        return True

    def __repr__(self):
        return_str = ""
        for i in range(3):
            for j in range(3):
                if self.array[i][j].is_empty():
                    return_str += "_"

                else:
                    return_str += self.array[i][j].symbol

            return_str += "\n"

        return return_str


def minimax(grid, depth, is_max, player_symbol, opp_symbol):
    score = evaluate(grid, player_symbol)

    if score == 10:
        return score

    if score == -10:
        return score

    if grid.is_full():
        return 0

    if is_max:
        best = -1000
        for column in grid.array:
            for piece in column:
                if piece.is_empty():
                    piece.set_symbol(player_symbol)
                    best = max(best, minimax(grid, depth + 1, False, player_symbol, opp_symbol))

                    piece.reset_symbol()

        return best

    else:
        best = 1000
        for column in grid.array:
            for piece in column:
                if piece.is_empty():
                    piece.set_symbol(opp_symbol)
                    best = min(best, minimax(grid, depth + 1, True, player_symbol, opp_symbol))

                    piece.reset_symbol()

        return best


def minimax_alpha_beta(grid, depth, is_max, player_symbol, opp_symbol, alpha=-1000, beta=1000):
    score = evaluate(grid, player_symbol)

    if score == 10:
        return score

    if score == -10:
        return score

    if grid.is_full():
        return 0

    if is_max:
        best = -1000
        for column in grid.array:
            for piece in column:
                if piece.is_empty():
                    piece.set_symbol(player_symbol)
                    best = max(best, minimax_alpha_beta(grid, depth + 1, False, player_symbol, opp_symbol, alpha, beta))
                    alpha = max(best, alpha)
                    piece.reset_symbol()
                    if beta <= alpha:
                        break

        return best

    else:
        best = 1000
        for column in grid.array:
            for piece in column:
                if piece.is_empty():
                    piece.set_symbol(opp_symbol)
                    best = min(best, minimax_alpha_beta(grid, depth + 1, True, player_symbol, opp_symbol, alpha, beta))
                    beta = min(best, beta)
                    piece.reset_symbol()
                    if beta <= alpha:
                        break

        return best


def find_best_move(grid, player="X", opp="O"):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if grid.array[i][j].is_empty():
                grid.array[i][j].set_symbol(player)

                move_val = minimax(grid, 0, False, player, opp)

                grid.array[i][j].reset_symbol()

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move


def find_best_move_alpha_beta(grid, player="X", opp="O"):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if grid.array[i][j].is_empty():
                grid.array[i][j].set_symbol(player)

                move_val = minimax_alpha_beta(grid, 0, False, player, opp)

                grid.array[i][j].reset_symbol()

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move


def evaluate(grid, symbol):
    status = grid.check_win()
    if status[0]:
        if status[1] == symbol:
            return 10

        else:
            return -10

    return 0


class Symbol:
    def __init__(self):
        self.symbol = None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def reset_symbol(self):
        self.symbol = None

    def is_empty(self):
        return self.symbol is None

    def __eq__(self, other):
        return not (not (self.symbol == other.symbol) or self.symbol is None)


def play_self():
    grid = Grid()
    while not (grid.check_win()[0] or grid.is_full()):
        p1_move = find_best_move(grid, "X", "O")
        if not p1_move == (-1, -1):
            grid.add_piece(p1_move[0], p1_move[1], "X")
        print(grid)
        input()
        p2_move = find_best_move(grid, "O", "X")
        if not p2_move == (-1, -1):
            grid.add_piece(p2_move[0], p2_move[1], "O")
        print(grid)
        input()


def measure_times():
    random.seed(0)
    grids = []
    for i in range(1000):
        grid = Grid()
        for column in grid.array:
            for piece in column:
                piece.set_symbol(random.choice(("X", "O", None)))

        grids.append(grid)
    start = time.time()
    for grid in grids:
        find_best_move(grid)

    return time.time() - start


def measure_times_alpha_beta():
    random.seed(0)
    grids = []
    for i in range(1000):
        grid = Grid()
        for column in grid.array:
            for piece in column:
                piece.set_symbol(random.choice(("X", "O", None)))

        grids.append(grid)

    start = time.time()
    for grid in grids:
        find_best_move_alpha_beta(grid)

    return time.time() - start


if __name__ == "__main__":
    x = Grid()
    print(measure_times())
    print(measure_times_alpha_beta())
