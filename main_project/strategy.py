from main_project.connect4_grid import Grid
from collections import defaultdict
import math
import random


class Strategy:
    def __init__(self, grid: Grid, player_symbol: str, depth: int, select_p: float):
        """
        Initialize the strategy.
        Parameters
        ----------
        grid: Grid
            The grid to use for this strategy.
        player_symbol: str
            The symbol of the player whose is making the move
        depth: int
            The depth to which the strategy should search
        select_p: float
            The probability that the strategy selects a move
        """
        self.symbol = player_symbol
        self.grid = grid
        self.evaluator = Evaluator(grid, player_symbol, depth)
        self.ranked_indices = []
        self.select_p: float = select_p

    def rank_moves(self):
        """
        Ranks the possible moves from best to worst
        Sets the value of self.ranked_indices to the indices ranked from best to worst.

        """
        self.evaluator.grid_to_int()
        values = self.evaluator.calculate_move_values()
        # We want moves with higher values to be ranked higher and then rank by depth.

        indexed_values = [(values[i][0], values[i][1], i) for i in range(len(values)) if not values[i] is None]
        # We shuffle the values to make all indexes equally likely before we start sorting
        random.shuffle(indexed_values)

        # This will sort the moves with value more important than length
        # Negative sign is because values are ranked in descending

        # If the move is positively ranked we want to choose the move with the lowest length.
        # If it is negatively ranked we want to choose the move with the highest length.
        # Moves with zero value should theoretically all have the same length, so it shouldn't matter.
        ranked_values = sorted(indexed_values,
                               key=lambda element: (-element[0], (-1 if element[0] < 0 else 1) * element[1]))
        self.ranked_indices = [value[2] for value in ranked_values]

    def move(self):
        """
        Function for determining which move the computer chooses.
        Returns
        -------
        The move the computer has made.

        """
        self.rank_moves()

        for move in self.ranked_indices:
            if random.random() < self.select_p:
                return move

        return random.choice(self.ranked_indices)


class Evaluator:
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
        self.is_default = (self.num_columns == 7) and (self.num_rows == 6)

        self._position: int = 0
        self._mask: int = 0
        self._full_grid = self.calculate_full_grid()
        self._depth = depth

        self.cache = defaultdict(lambda: (None, None))

        self.move_values: list = []

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
        """
        Gets the position stored in the evaluator.
        Returns
        -------
        int:
            the position

        """
        return self._position

    def get_mask(self):
        """
        Gets the mask stored in the evaluator
        Returns
        -------
        int:
            the mask

        """
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
        if n == 4:

            shift = position & base_shift
            if shift & (shift >> (self.num_rows * 2 + 2)):
                return True

            # Diagonal \
            shift = position & (base_shift << 1)
            if shift & (shift >> (self.num_rows * 2)):
                return True

            # Diagonal /
            shift = position & (base_shift >> 1)
            if shift & (shift >> ((self.num_rows * 2) + 4)):
                return True

            # Vertical
            shift = position & (position >> 1)
            if shift & (shift >> 2):
                return True

        if n == 3:
            shift = position & base_shift
            if shift & (shift >> (self.num_rows + 1)):
                return True

            shift = position & (base_shift << 1)
            if shift & (shift >> self.num_rows):
                return True

            shift = position & (base_shift >> 1)
            if shift & (shift >> (self.num_rows + 2)):
                return True

            shift = position & (position >> 1)
            if shift & (shift >> 1):
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
        return new_mask, new_position, new_position ^ mask

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

    def minimax_alpha_beta(self, mask: int, position: int, is_max: bool, depth: int, alpha: float,
                           beta: float):
        """
        Recursively checks the possible board from the current states and evaluates them.
        Parameters
        ----------
        mask: int
            The mask of the grid.
        position: int
            The position of the grid.
        is_max: int
            Whether it is maximising or minimising.
        depth: int
            The depth to check up to.
        alpha: float
        beta: float

        Returns
        -------
        tuple
            The value of the board and how far away it terminates.

        """
        if self.check_n_in_a_row(position ^ mask):  # Since we are receiving after the opposing player has made a
            # move we can guarantee that wew don't have a 4-in-a-row
            if is_max:
                return -math.inf, 0

            return math.inf, 0

        if mask == self._full_grid:
            return 0, 0  # If the grid is full we return 0 since that means it is a draw.

        if depth == 0:
            return ((-1) ** (not is_max)) * (self.evaluate_grid(position) - self.evaluate_grid(position ^ mask)), 0

        next_states = []
        for column in range(self.num_columns):
            # Find all possible states that aren't full. May be more efficient to do this part in 1 loop with the rest.
            if not self.check_bit(mask, column, 0):
                next_states.append(self.make_move(mask, position, column))

        if is_max:
            best = -math.inf
        else:
            best = math.inf

        current_length = 0
        for state in next_states:
            cached_value = self.get_cache(state[0], state[1], depth - 1)
            if cached_value is False:
                val_length = self.minimax_alpha_beta(state[0], state[1], not is_max, depth - 1, alpha, beta)
                val = val_length[0]
                length = val_length[1]

                self.set_cache(state[0], state[1], (-1) ** (not is_max) * cached_value, length)

            else:
                val = cached_value[0]
                length = cached_value[1]

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

    def calculate_move_values(self) -> list:
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
                    self.move_values.append(self.minimax_alpha_beta(move[0], move[1], False, self._depth,
                                                                    -math.inf, math.inf))

        return self.move_values

    def evaluate_self(self):
        """
        Runs the minimax algorithm on the values stored in self._mask and self._position
        Returns
        -------
        float:
            The value of the grid described by self._mask and self._position.

        """

        return self.minimax_alpha_beta(self._mask, self._position, True, self._depth, -math.inf, math.inf)

    def calculate_full_grid(self):
        """
        Calculates the integer value of a full grid.
        Returns
        -------
        int
            The integer value of the full grid

        """
        grid_list = [["0"] + ["1" for i in range(self.num_rows)] for j in range(self.num_columns)]
        grid_str = "".join("".join(row) for row in grid_list)
        return int(grid_str, 2)

    def get_cache(self, mask, pos, depth):
        """
        Returns the cached value for the mask and position if one exists and returns False if it doesn't
        Parameters
        ----------
        mask: int
            the mask of the grid
        pos: int
            the pos of the grid
        depth: int
            the depth of the current search

        Returns
        -------
        list[int]
            The cached value stored

        """
        cached_value = self.cache[(mask, pos)]
        if self.cache[(mask, pos)][0] is None:
            return False  # If it does not exist then return False

        elif cached_value[1] < depth:
            return False  # If the stored depth is less than the desired then we should do the search again

        return cached_value

    def set_cache(self, mask: int, pos: int, value: int, depth: int):
        """
        Sets the value of the cache based off the mask and position
        Parameters
        ----------
        mask: int
            the mask of the grid
        pos: int
            the pos of the grid
        value: int
            the calculated value for the grid
        depth: int
            the depth of the search

        """
        self.cache[(mask, pos)] = (value, depth)

    def evaluate_grid(self, position):
        """
        Evaluates a grid based on how close to the middle the bits are
        Parameters
        ----------
        position: int
            The position of the grid to evaluate.

        Returns
        -------
        int:
            the estimate for the value of the grid

        """
        if not self.is_default:
            # If it is not a 7x6 grid return 0 as a heuristic will not be used
            return 0
        weights = [[3, 4, 5, 7, 5, 4, 3],
                   [4, 6, 8, 10, 8, 6, 4],
                   [5, 8, 11, 13, 11, 8, 5],
                   [5, 8, 11, 13, 11,  8, 5],
                   [4, 6, 8, 10, 8, 6, 4],
                   [3, 4, 5, 7, 5, 4, 3]]

        total = 0
        for column in range(7):
            for row in range(6):
                total += weights[row][column] * self.check_bit(position, column, row)

        return total


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
        output_list = self.grid_list(grid_int)

        return "".join(["".join(column_list) + "\n" for column_list in output_list])

    def grid_list(self, grid_int: int):
        """
        Converts the input value into an array of ones and zeros
        Parameters
        ----------
        grid_int: int
            The binary number to convert.

        Returns
        -------
        list[list[int]]
            The list of ones and zeros

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

        return output_list

    def get_grid(self, op_symbol):
        """
        Converts self._position and self._mask into a grid class, used for debugging.
        Parameters
        ----------
        op_symbol:
            The symbol of the opposing player

        Returns
        -------
        Grid:
            The Grid representing the mask and position

        """
        player_output_list = self.grid_list(self._position)
        op_output_list = self.grid_list(self._mask ^ self._position)
        new_grid = Grid(self.num_rows, self.num_columns, self.grid.win_num)

        for i in range(len(player_output_list)):
            for j in range(len(player_output_list)):
                if i != 0:
                    if player_output_list[i][j] == "1":
                        new_grid.set_cell(self.num_rows - i, j, self.player_symbol)

                    elif op_output_list[i][j] == "1":
                        new_grid.set_cell(self.num_rows - i, j, op_symbol)

        return new_grid


if __name__ == "__main__":
    pass

