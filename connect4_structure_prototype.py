class Grid:
    def __init__(self, num_rows=6, num_columns=7, win_num=5):
        self.win_num = win_num
        self.num_rows = num_rows
        self.num_columns = num_columns

        self.cells = {(i, j): Cell(i, j) for i in range(self.num_rows) for j in range(self.num_columns)}

        self.columns = [[(j, i) for i in range(self.num_rows)] for j in range(self.num_columns)]

        self.rows = [[(i, j) for j in range(self.num_columns)] for i in range(self.num_rows)]

        self.SW_diagonals = [[(i, j) for i in range(self.num_rows) for j in range(self.num_columns) if i + j == k]
                             for k in range(2 * min(self.num_columns, self.num_rows))]

        self.SE_diagonals = [
            [(i, self.num_columns - j - 1) for i in range(self.num_rows) for j in range(self.num_columns) if i + j == k]
            for k in range(2 * min(self.num_columns, self.num_rows))]

        self.all_lines = self.columns + self.rows + self.SW_diagonals + self.SE_diagonals

    def check_win(self):
        pass

    def check_line(self, line):
        pass


class Cell:
    def __init__(self, i, j):
        self.row = i
        self.column = j
        self.symbol = None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return not (not (self.symbol == other.symbol) or self.symbol is None)

    def __repr__(self):
        return f"Cell({self.row}, {self.column}, {self.symbol})"


if __name__ == "__main__":
    grid = Grid()
