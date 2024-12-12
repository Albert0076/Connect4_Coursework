from connect4_structure_prototype import Grid
import random

class Strategy:
    def __init__(self, grid: Grid, player_symbol: str):
        self.symbol = player_symbol
        self.grid = grid


    def move(self):
        pass



class VeryEasy(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)


    def move(self):
        return random.choice([column for column in self.grid.columns if not self.grid.line_full(column)])



class Easy(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)


    def move(self):
        pass


class Medium(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)

    def move(self):
        pass


class Hard(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)

    def move(self):
        pass


class Evaluator:
    def __init__(self, grid: Grid, player_symbol: str):
        """
        Parameters
        ----------
        grid : Grid
            The grid of the board to analyze.
        player_symbol: str
            The symbol of the player who moves first.

        """
        self.grid = grid
        self.player_symbol = player_symbol


        self._position: int = 0
        self._mask: int = 0




    def grid_to_int(self):
        """
        Converts a grid object into position and mask numbers.

        """
        position = ''
        mask = ''
        # The grid is represented with a position and a mask. To find the other position we can XOR the two
        for column in range(self.grid.num_columns):
            mask += "0"
            position += "0"
            for row in range(self.grid.num_rows-1, -1, -1):
                # We add to the mask if the cell is not empty
                mask += ['0', '1'][not self.grid.cells[(row, column)].is_empty()]
                # We add to the position if the cell has the desired symbol
                position += ['0', '1'][self.grid.cells[(row, column)].symbol == self.player_symbol]


        # Each column is represented with a binary number with a length of one more than the column height and the msb being 0
        # The grid is then represented with one binary number with the rightmost column being at the end of the number


        self._position = int(position, 2)
        self._mask = int(mask, 2)

    def get_position(self):
        return self._position

    def get_mask(self):
        return self._mask


    def check_n_in_a_row(self):
        """
        Checks if the current position contains an n in a row.
        Returns
        -------
        bool
            Whether the current position contains an n in a row.

        """
        base_shift = self._position >> self.grid.num_rows+1 # Same as a horizontal shift of 1
        # This only works with four in a row for now
        # Horizontal
        shift = self._position & base_shift
        if shift & (shift >> (self.grid.num_rows+1)*2) :
            return True

        # Diagonal \
        shift = self._position & (base_shift << 1)
        if shift & (shift >> self.grid.num_rows * 2):
            return True

        # Diagonal /
        shift = self._position & (base_shift >> 1)
        if shift & (shift >> (self.grid.num_rows+2) * 2):
            return True

        # Vertical
        shift = self._position & (self._position >> 1)
        if shift & (shift >> 2):
            return True


        return False


    def make_move(self, column):
        """
        Updates the current position and mask based on the move just made.
        Parameters
        ----------
        column: int
            The column where the move is made.

        """
        self._position = self._position ^ self._mask # Changes the position to the other player
        self._mask = self._mask | (self._mask + (1 << (self.grid.num_columns-1-column) * (self.grid.num_rows+1)))


    def __repr__(self):
        return Evaluator(grid=self.grid, player_symbol=self.player_symbol)


    def print_grid(self, mask=True):
        """
        Prints the integer version of the grid in a readable format.
        Parameters
        ----------
        mask: bool
            Whether we want to return the mask or the position.

        Returns
        -------
        str
            The formatted grid.

        """
        # We are seeing if we want to return the mask or the position
        if mask:
            grid_to_convert = self._mask

        else:
            grid_to_convert = self._position

        mask_str = format(grid_to_convert, f'0{self.grid.num_columns * (self.grid.num_rows+1)}b')
        output_list = [[" " for __ in range(self.grid.num_columns)] for _ in range(self.grid.num_rows+1)]
        i, j = self.grid.num_rows, 0
        for symbol in mask_str:
            i = (i+1) % (self.grid.num_rows+1)
            output_list[i][j] = symbol
            if i == self.grid.num_rows:
                j +=1

        return "".join(["".join(column_list) + "\n" for column_list in output_list])


if __name__ == "__main__":
    grid = Grid(4, 4, 4)
    evaluator = Evaluator(grid=grid, player_symbol="R")
    evaluator.grid_to_int()
    evaluator.make_move(1)
    print(evaluator.print_grid())
    print(evaluator.print_grid(False))



