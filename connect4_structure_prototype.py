class Grid:
    def __init__(self, num_rows=6, num_columns=7, win_num=4):
        self.win_num = win_num
        self.num_rows = num_rows
        self.num_columns = num_columns

        self.cells = {(i, j): Cell(i, j) for i in range(self.num_rows) for j in range(self.num_columns)}

        self.columns = [[(i, j) for i in range(self.num_rows)] for j in range(self.num_columns)]

        self.rows = [[(i, j) for j in range(self.num_columns)] for i in range(self.num_rows)]

        self.SW_diagonals = [[(i, j) for i in range(self.num_rows) for j in range(self.num_columns) if i + j == k]
                             for k in range(2 * min(self.num_columns, self.num_rows))]

        self.SE_diagonals = [
            [(i, self.num_columns - j - 1) for i in range(self.num_rows) for j in range(self.num_columns) if i + j == k]
            for k in range(2 * min(self.num_columns, self.num_rows))]

        self.all_lines = self.columns + self.rows + self.SW_diagonals + self.SE_diagonals

    def add_piece(self, column, symbol):
        added = False
        count = 0
        while not added and count < self.num_columns:
            if self.cells[self.columns[column][count]].is_empty():
                added = True
                self.cells[self.columns[column][count]].set_symbol(symbol)

            else:
                count += 1

        return added

    def check_win(self):
        for line in self.all_lines:
            checked_line = self.check_line(line)
            if checked_line[0]:
                return checked_line

        return False, None

    def check_line(self, line):
        if len(line) < self.win_num:
            return False, None

        else:
            for i in range(len(line) - self.win_num):
                won = True
                for j in range(self.win_num - 1):
                    if self.cells[line[i + j]] != self.cells[line[i + j + 1]]:
                        won = False

                if won:
                    return True, self.cells[line[i]].symbol

        return False, None

    def __repr__(self):
        return f"Grid({self.num_rows=}, {self.num_columns=}, {self.win_num=})"

    def __str__(self):
        return_str = ""
        for i in range(len(self.rows) - 1, -1, -1):
            for cell in self.rows[i]:
                if self.cells[cell].is_empty():
                    return_str += "_ "

                else:
                    return_str += self.cells[cell].symbol[0] + " "

            return_str += "\n"

        for i in range(len(self.columns)):
            return_str += f"{i + 1} "

        return return_str


class Cell:
    def __init__(self, i, j):
        self.row = i
        self.column = j
        self.symbol = None

    def is_empty(self):
        return self.symbol is None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return self.symbol == other.symbol and not self.symbol is None

    def __repr__(self):
        return f"Cell({self.row}, {self.column}, {self.symbol})"


if __name__ == "__main__":
    grid = Grid()
    for i in range(4):
        for j in range(i):
            grid.add_piece(i, "Yellow")

        grid.add_piece(i, "Red")


    print(grid)
    print(grid.check_win())