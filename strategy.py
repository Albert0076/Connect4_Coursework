from connect4_structure_prototype import Grid
import random


class Strategy:
    def __init__(self, grid: Grid, player_symbol: str, depth: int, select_p: float):
        self.symbol = player_symbol
        self.grid = grid
        self.evaluator = Evaluator(grid, player_symbol, depth)
        self.ranked_indices = []
        self.select_p: float = select_p  # The probability a given value will be selected

    def rank_moves(self):
        """
        Ranks the possible moves from best to worst
        Sets the value of self.ranked_indices to the indices ranked from best to worst.

        """
        self.evaluator.grid_to_int()
        self.evaluator.calculate_move_values()
        # We want moves with higher values to be ranked higher and then rank by depth.
        values = self.evaluator.move_values

        indexed_values = [(values[i][0], values[i][1], i) for i in range(len(values)) if not values[i] is None]
        # We shuffle the values to make all indexes equally likely before we start sorting
        random.shuffle(indexed_values)

        # This will sort the moves with value more important than length
        # Negative sign is because values are ranked in descending
        ranked_values = sorted(indexed_values, key=lambda element: (-element[0], element[1]))
        self.ranked_indices = [value[2] for value in ranked_values]

    def move(self):
        """
        Function for determining which move the computer chooses.
        Returns
        -------
        The move the computer has made.

        """
        self.evaluator.grid_to_int()
        self.evaluator.calculate_move_values()

        #Need to finish


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

        self.move_values = []

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

        # Each column is represented with a binary number with a length of one more than the column height and the
        # msb being 0.
        # The grid is then represented with one binary number with the rightmost column being at the end
        # of the number.

        if self._position != int(position, 2) or self._mask != int(mask, 2):
            self._position = int(position, 2)
            self._mask = int(mask, 2)
            self.move_values = []

    def get_position(self):
        return self._position

    def get_mask(self):
        return self._mask

    def check_n_in_a_row(self, position: int, n=4):
        """
        Checks if the current position contains an n in a row.
        Parameters
        ----------
        n: int
            The number in a row we are checking.
        position: int
            The position to check.

        Returns
        -------
        bool
            Whether the current position contains an n in a row.

        """
        base_shift = position >> self.num_rows + 1  # Same as a horizontal shift of 1
        # This only works with four/three in a row.
        # Horizontal
        shift = position & base_shift
        if shift & (shift >> (self.num_rows + 1) * n - 2):
            return True

        # Diagonal \
        shift = position & (base_shift << 1)
        if shift & (shift >> self.num_rows * n - 2):
            return True

        # Diagonal /
        shift = position & (base_shift >> 1)
        if shift & (shift >> (self.num_rows + 2) * n - 2):
            return True

        # Vertical
        shift = position & (position >> 1)
        if shift & (shift >> n - 2):
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
            # Whether current player has n-1 in a row
            n_minus_1_self = self.check_n_in_a_row(position, self.grid.win_num - 1)
            # Whether opposing player has n-1 in a row
            n_minus_1_op = self.check_n_in_a_row(op_position, self.grid.win_num - 1)

            if is_max:
                return n_minus_1_self * 5 - n_minus_1_op * 5, 0

            return -(n_minus_1_self * 5 - n_minus_1_op * 5), 0

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
                if val > best:  # If we find a new best value we change best and also change the length.
                    best = val
                    current_length = length  # The minimax algorithm doesn't care about the length, useful for strategy.
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
        if not self.move_values:
            for column in range(self.num_columns):
                if self.check_bit(self._mask, column, 0):
                    self.move_values.append(None)  # We really don't want anything selecting a column that is too full

                else:
                    move = self.make_move(self._mask, self._position, column)
                    self.move_values.append(self.minimax_alpha_beta(move[0], move[1], 0, False, self._depth,
                                                                    -Evaluator.MAX, Evaluator.MAX))

        return self.move_values

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
        grid.add_piece(2, "R")
    strategy = Strategy(grid, "R", 11, 1.0)
    strategy.rank_moves()
    print(strategy.ranked_indices)