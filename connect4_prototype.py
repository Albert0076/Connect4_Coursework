import pyinputplus


class Grid:
    def __init__(self, columns, rows, win_num):
        self.columns = columns
        self.rows = rows
        self.win_num = win_num
        self.grid = [[Piece(i, j) for j in range(self.rows)] for i in range(self.columns)]

    def add_piece(self, column, colour):
        placed = False
        for piece in self.grid[column]:
            if piece.is_empty() and not placed:
                piece.colour = colour
                placed = True

        if not placed:
            raise IndexError("Column is full")

    def reset(self):
        for column in self.grid:
            for piece in column:
                piece.reset()

    def get_top(self, column):
        for i in range(self.rows - 1, -1, -1):
            if not self.grid[column][i].is_empty():
                return self.grid[column][i]

        return None

    def get_piece(self, column, row):
        return self.grid[column][row]

    def check_winning_move(self, piece):
        for i in range(max(0, piece.column - self.win_num), min(piece.column, self.columns - self.win_num) + 1):
            winning_move = True
            for j in range(self.win_num - 1):
                if self.grid[i + j][piece.row] != self.grid[i + j + 1][piece.row]:
                    winning_move = False

            if winning_move:
                return True

        for i in range(max(0, piece.row - self.win_num), min(piece.row, self.rows - self.win_num) + 1):
            winning_move = True
            for j in range(self.win_num - 1):
                if self.grid[piece.column][i + j] != self.grid[piece.column][i + j + 1]:
                    winning_move = False

            if winning_move:
                return True
        diag_start = min(piece.column, piece.row, self.win_num)
        for i in range(diag_start + 1):
            winning_move = True
            for j in range(self.win_num - 1):
                add_amount = i + j - diag_start
                if (self.grid[piece.column + add_amount][piece.row + add_amount]
                        != self.grid[piece.column + add_amount + 1][piece.row + add_amount + 1]):
                    winning_move = False

            if winning_move:
                return True

        diag_start = min(self.win_num, self.columns - piece.column, piece.row)
        for i in range(diag_start + 1):
            winning_move = True
            for j in range(self.win_num - 1):
                add_amount = i + j - diag_start
                if (self.grid[piece.column - add_amount][piece.row + add_amount] !=
                        self.grid[piece.column - add_amount - 1][piece.row + add_amount + 1]):
                    winning_move = False

            if winning_move:
                return True

        return False

    def __repr__(self):
        return f"Grid(columns: {self.columns}, rows: {self.rows}, win_num: {self.win_num})"

    def __str__(self):
        return_str = ""
        for i in range(self.rows - 1, -1, -1):
            for j in range(self.columns):
                if not self.grid[j][i].is_empty():
                    return_str += self.grid[j][i].colour[0]

                else:
                    return_str += "_"

                return_str += " "

            return_str += "\n"

        return return_str


class Piece:
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.colour = None

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour

    def reset(self):
        self.colour = None

    def is_empty(self):
        return self.colour is None

    def __eq__(self, other):
        return self.colour == other.colour

    def __repr__(self):
        return f"Piece({self.colour})"


class Game:
    def __init__(self, interface, columns=7, rows=6, win_num=4):
        self.grid = Grid(columns, rows, win_num)
        self.columns = columns
        self.rows = rows
        self.win_num = win_num
        self.players = []
        self.interface = interface

    def add_human_player(self, colour, name):
        self.players.append(HumanPlayer(colour, name))

    def make_move(self, player):
        colour = player.colour
        column = player.get_column()
        self.grid.add_piece(column, colour)
        if self.grid.check_winning_move(self.grid.get_top(column)):
            self.game_won(player)

    def game_won(self, player):
        pass

    def reset(self):
        self.grid.reset()

    def main_loop(self):
        for player in self.players:
            if isinstance(HumanPlayer, player):
                move = self.interface.get_move(player)


class Player:
    def __init__(self, colour, name):
        self.colour = colour
        self.wins = 0
        self.name = name


class HumanPlayer(Player):
    def __init__(self, colour, name):
        super().__init__(colour, name)


class CLI:
    def __init__(self):
        self.game = None

    def setup(self):
        print("Welcome to Connect4!")
        user_default = pyinputplus.inputBool("Do you want to use default rules?", "Yes", "No")
        if not user_default:
            columns = pyinputplus.inputInt("Enter columns: ", min=1)
            rows = pyinputplus.inputInt("Enter rows: ", min=1)
            win_num = pyinputplus.inputInt("Enter number of pieces needed to win", min=1)
            self.game = Game(columns, rows, win_num)

        else:
            self.game = Game(self)

    def get_move(self, player):
        pass


if __name__ == "__main__":
    grid = Grid(4, 4, 2)
    grid.add_piece(0, "blue")
    grid.add_piece(0, "red")
    grid.add_piece(1, "red")
    x = grid.get_piece(0, 1)
    print(grid)
    print(grid.check_winning_move(x))
