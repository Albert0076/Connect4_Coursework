class Grid:
    def __init__(self):
        self.array = [[Symbol() for i in range(3)] for j in range(3)]

    def place_piece(self, symbol, column, row):
        self.array[column][row].set_symbol(symbol)

    def check_win(self):
        for i in range(3):
            if self.array[i][0] == self.array[i][1] == self.array[i][2]:
                return True

            if self.array[0][i] == self.array[1][i] == self.array[2][i]:
                return True

        if self.array[0][0] == self.array[1][1] == self.array[2][2]:
            return True

        if self.array[2][0] == self.array[1][1] == self.array[0][2]:
            return True

        return False


class Symbol:
    def __init__(self):
        self.symbol = None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return not (not (self.symbol == other.symbol) or self.symbol is None)
