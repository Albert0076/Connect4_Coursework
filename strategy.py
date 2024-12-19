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
    MAX = 10

    def __init__(self, grid: Grid, player_symbol: str, depth: int):
        """
        Parameters
        ----------
        grid : Grid
            The grid of the board to analyze.
        player_symbol: str
            The symbol of the player who moves first.

        depth: int
            The depth it will evaluate to.

        """
        self.grid = grid
        self.num_columns = self.grid.num_columns
        self.num_rows = self.grid.num_rows
        self.player_symbol = player_symbol

        self._position: int = 0
        self._mask: int = 0
        self._full_grid = self.calculate_full_grid()
        self._depth = depth

        self.values = []

    def grid_to_int(self):
        """
        Converts a grid object into position and mask numbers.

        """
        position = ''
        mask = ''
        # The grid is represented with a position and a mask. To find the other position we can XOR the two
        for column in range(self.num_columns):
            mask += "0"
            position += "0"
            for row in range(self.num_rows - 1, -1, -1):
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

    def check_n_in_a_row(self, position: int):
        """
        Checks if the current position contains an n in a row.
        Parameters
        ----------
        position: int
            The position to check.

        Returns
        -------
        bool
            Whether the current position contains an n in a row.

        """
        base_shift = position >> self.num_rows + 1  # Same as a horizontal shift of 1
        # This only works with four in a row for now
        # Horizontal
        shift = position & base_shift
        if shift & (shift >> (self.num_rows + 1) * 2):
            return True

        # Diagonal \
        shift = position & (base_shift << 1)
        if shift & (shift >> self.num_rows * 2):
            return True

        # Diagonal /
        shift = position & (base_shift >> 1)
        if shift & (shift >> (self.num_rows + 2) * 2):
            return True

        # Vertical
        shift = position & (position >> 1)
        if shift & (shift >> 2):
            return True

        return False

    def make_move(self, mask: int, position: int, column: int):
        """
        Returns new position and mask based on the input position and mask.
        Parameters
        ----------
        mask: int
            The mask of the grid.
        position: int
            The position of the grid.
        column: int
            The column where the move is made.

        """
        new_position = position ^ mask  # Changes the position to the other player
        new_mask = mask | (mask + (1 << (self.num_columns - 1 - column) * (self.num_rows + 1)))
        return new_mask, new_position, position

    def check_bit(self, mask: int, column: int, row: int):
        """
        Checks whether a specific bit is 1 or 0.
        Parameters
        ----------
        mask: int
            The mask of the grid.
        column: int
            The column to check.
        row: int
            The row to check, counts from the top.

        Returns
        -------
        bool
            Whether the bit is 0 or 1.

        """
        shift = self.num_rows + 1
        # Row = -1 is to check if the column is invalid and row = 0 checks if the column is full.
        # Checking whether the top row of a column has a bit by doing an and with a bit in that column
        return bool(mask & (1 << (shift * (self.num_columns - column) - (row + 2))))

    def minimax_alpha_beta(self, mask: int, position: int, op_position: int, is_max: bool, depth: int, alpha: int,
                           beta: int):
        """
        Recursively checks the possible board from the current states and evaluates them.
        Parameters
        ----------
        mask: int
            The mask of the grid.
        position: int
            The position of the grid.

        op_position: int
            The position of the opponent grid.
        is_max: int
            Whether it is maximising or minimising.
        depth: int
            The depth to check up to.
        alpha: int
        beta: int

        Returns
        -------
        tuple
            The value of the board and how far away it terminates.

        """
        if self.check_n_in_a_row(op_position):  # Since we are receiving after the opposing player has made a move we
            # can guarantee that wew don't have a 4-in-a-row
            if is_max:
                return -Evaluator.MAX, 0

            return Evaluator.MAX, 0

        if mask == self._full_grid:
            return 0, 0  # If the grid is full we return 0 since that means it is a draw.

        if depth == 0:
            return 0, 0  # If the depth is 0 we are treating it as a draw but may have more sophisticated method later

        next_states = []
        for column in range(self.num_columns):
            # Find all possible states that aren't full. May be more efficient to do this part in 1 loop with the rest.
            if not self.check_bit(mask, column, 0):
                next_states.append(self.make_move(mask, position, column))

        if is_max:
            best = -Evaluator.MAX
        else:
            best = Evaluator.MAX

        current_length = 0
        for state in next_states:
            minimaxed = self.minimax_alpha_beta(state[0], state[1], state[2], not is_max, depth - 1, alpha, beta)
            val = minimaxed[0]
            length = minimaxed[1]

            if is_max:
                if val > best:
                    best = val
                    current_length = length
                alpha = max(best, alpha)
                if beta <= alpha:
                    return alpha, current_length + 1  # We increase the length the end is away by one.

            else:
                if val < best:
                    best = val
                    current_length = length
                beta = min(best, beta)
                if beta <= alpha:
                    return beta, current_length + 1

        return best, current_length + 1

    def calculate_move_values(self):
        """
        Calculates the value of all possible moves from the position and mask.
        Returns
        -------
        list
            The value of a move at each of the different columns.

        """
        if not self.values:
            for column in range(self.num_columns):
                if self.check_bit(self._mask, column, 0):
                    self.values.append(None)  # We really don't want anything selecting a column that is too full

                else:
                    move = self.make_move(self._mask, self._position, column)
                    self.values.append(self.minimax_alpha_beta(move[0], move[1], 0, False, self._depth,
                                                               -Evaluator.MAX, Evaluator.MAX))

        return self.values

    def calculate_full_grid(self):
        grid_list = [["0"] + ["1" for i in range(self.num_rows)] for j in range(self.num_columns)]
        grid_str = "".join("".join(row) for row in grid_list)
        return int(grid_str, 2)

    def __repr__(self):
        return f"Evaluator({self.grid=}, {self.player_symbol=})"

    def print_grid(self, grid_int: int):
        """
        Prints the integer version of the grid in a readable format.
        Parameters
        ----------
        grid_int: int
            The grid we want to print.

        Returns
        -------
        str
            The formatted grid.

        """
        # We are seeing if we want to return the mask or the position
        grid_to_convert = grid_int
        # Get a binary string of the length we want so we can easily print it:
        mask_str = format(grid_to_convert, f'0{self.grid.num_columns * (self.grid.num_rows + 1)}b')
        output_list = [[" " for __ in range(self.grid.num_columns)] for _ in range(self.grid.num_rows + 1)]
        row, column = self.grid.num_rows, 0
        for symbol in mask_str:
            # We decrease the row and then the column once the row has looped
            row = (row + 1) % (self.grid.num_rows + 1)
            output_list[row][column] = symbol
            if row == self.grid.num_rows:
                column += 1

        return "".join(["".join(column_list) + "\n" for column_list in output_list])


if __name__ == "__main__":
    grid = Grid(6, 7, 4)
    for i in range(3):
        grid.add_piece(0, "R")

    evaluator = Evaluator(grid, "R", 11)
    evaluator.grid_to_int()

    evaluator.calculate_move_values()
    print(evaluator.values)
