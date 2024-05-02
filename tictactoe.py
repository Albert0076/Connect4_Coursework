class Grid:
    def __init__(self):
        self.array = [[Symbol() for j in range(3)] for i in range(3)]

    def add_piece(self, column, row, symbol):
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

            return_str += ("\n")

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
        return self.symbol == other.symbol and not self.symbol is None


if __name__ == "__main__":
    x = Grid()
    print(x)
    print(find_best_move(x))
