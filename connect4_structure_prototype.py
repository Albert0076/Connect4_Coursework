class Grid:
    def __init__(self, num_rows=6, num_columns=7, win_num=4):
        """
        Parameters
        ----------
        num_rows: int
            The number of rows in the grid.
        num_columns: int
            The number of columns in the grid.
        win_num: int
            The number of symbols in a row needed to win.
        """
        self.win_num = win_num
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.winning_symbol = None

        # Cells ares stored in a dictionary, with a tuple of coordinates as the key and the Cell class as the data
        self.cells = {(row, column): Cell(row, column) for row in range(self.num_rows) for column in range(self.num_columns)}

        # The rows, columns and diagonals are then stored as lists of tuples which can then be checked in the dictionary
        self.columns = [[(row, column) for row in range(self.num_rows)] for column in range(self.num_columns)]

        self.rows = [[(row, column) for column in range(self.num_columns)] for row in range(self.num_rows)]

        self.SW_diagonals = [[(row, column) for row in range(self.num_rows) for column in range(self.num_columns) if row + column == k]
                             for k in range(2 * min(self.num_columns, self.num_rows))]

        self.SE_diagonals = [
            [(row, self.num_columns - column - 1) for row in range(self.num_rows) for column in range(self.num_columns) if row + column == k]
            for k in range(2 * min(self.num_columns, self.num_rows))]

        self.all_lines = self.columns + self.rows + self.SW_diagonals + self.SE_diagonals

    def column_height(self, column: int):
        """
        Returns the number of pieces in a column.

        Parameters
        ----------
        column: int
            The column in the grid.

        Returns
        -------
        int
            The height of the column.

        """
        if not (isinstance(column, int) and -1 <= column <= self.num_columns):
            raise ValueError
        return sum([1 if not self.cells[cell].is_empty() else 0 for cell in self.columns[column]])

    def add_piece(self, column: int, symbol: str):
        """
        Adds a piece to a column in the grid.

        Parameters
        ----------
        column: int
            The column the piece is being added too.
        symbol: str
            The symbol of the piece being added.

        Raises
        ------
        IndexError
            If the column is full or not on the grid.

        """
        added = False
        count = 0
        # Loop up the column until a free cell is encountered and then stop looping up
        while not added and count < self.num_columns:
            if self.cells[self.columns[column][count]].is_empty():
                added = True
                self.cells[self.columns[column][count]].set_symbol(symbol)

            else:
                count += 1

        if not added:
            # If it loops through the column without finding an empty cell it will raise an IndexError
            raise IndexError("Column is full.")

    def check_win(self):
        """
        Checks to see if the grid has an n in a row.
        Returns
        -------
        bool
            whether the grid has an n in a row.

        """
        # Check line on all the lines and then see if any of them have a win
        return any([self.check_line(line) for line in self.all_lines])

    def check_line(self, line: list):
        """
        Checks to see if a line has an n in a row.
        Parameters
        ----------
        line: list
            The line to check.

        Returns
        -------
        bool
            whether the line has an n in a row.

        """
        if len(line) < self.win_num:
            # If the length of the line is less than the win length we know it cannot have a win
            return False

        else:
            for start_index in range(len(line) - self.win_num + 1):
                # We loop through from the first position in the line, up to the last one where a win could still be
                # possible
                won = all([self.cells[line[start_index]] == self.cells[line[start_index + relative_index]] for relative_index in range(self.win_num)])

                if won:
                    # If a line has n in a row we find the winning symbol and then return True
                    # One potential issue with this system is that we cannot detect if there are two different wins from
                    # different players however the logic of the game should prevent this from happening
                    self.winning_symbol = self.cells[line[start_index]].symbol
                    return True

        return False

    def line_full(self, line):
        """
        Checks to see if a line is full.
        Parameters
        ----------
        line: list
            The line to check.

        Returns
        -------
        bool
            Whether the line is full.

        """
        return all([self.cells[position].is_empty() for position in line])

    def grid_full(self):
        """
        Checks to see if the grid is full.
        Returns
        -------
        bool
            Whether the grid is full.

        """
        return all([self.line_full(line) for line in self.all_lines])

    def set_cell(self, row, column, symbol):
        self.cells[(row, column)].set_symbol(symbol)

    def __repr__(self):
        """
        __repr__ function for grid.
        Returns
        -------
        str
            Grid(num_rows, num_columns, win_num)

        """
        return f"Grid({self.num_rows=}, {self.num_columns=}, {self.win_num=})"

    def __str__(self):
        """
        __str__ function which shows the grid in an understandable way.
        Returns
        -------
        str
            All the cells including end lines

        """
        return_str = ""
        for row in range(len(self.rows) - 1, -1, -1):
            for cell in self.rows[row]:
                if self.cells[cell].is_empty():
                    return_str += "|_| "

                else:
                    return_str += "|" + self.cells[cell].symbol[0] + "| "

            return_str += "\n"

        for row in range(len(self.columns)):
            return_str += f" {row + 1}  "

        return return_str


class Cell:
    def __init__(self, row: int, column: int):
        """
        Parameters
        ----------
        row: int
            The row of the cell.
        column: int
            The column of the cell.

        """
        self.row = row
        self.column = column
        self.symbol = None

    def is_empty(self):
        """
        Checks if the cell is empty.
        Returns
        -------
        bool
            Whether the symbol of the cell is none.

        """
        return self.symbol is None

    def set_symbol(self, symbol: str):
        """
        Sets the symbol of the cell.
        Parameters
        ----------
        symbol: str
            The symbol of the cell.

        """
        self.symbol = symbol

    def __eq__(self, other):
        """
        Checks to see if too cells have the same symbol.
        Parameters
        ----------
        other: Cell
            The other cell to check.

        Returns
        -------
        bool
            Whether the symbols of the cells are equal and not None.

        """
        return self.symbol == other.symbol and not self.symbol is None

    def __repr__(self):
        """
        __repr__ function for cell.
        Returns
        -------
        str
            Cell(row=, column=, symbol=)

        """
        return f"Cell({self.row=}, {self.column=}, {self.symbol=})"


if __name__ == "__main__":
    grid = Grid()
    for i in range(4):
        for j in range(i):
            grid.add_piece(i, "Yellow")

        grid.add_piece(i, "Red")




    print(grid)
    print(grid.check_win())
