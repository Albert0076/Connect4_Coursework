from connect4_structure_prototype import Grid
import copy
import random
from binary_string_minimax_test import find_best_move, get_bit_mask
from strategy import Strategy, Evaluator


class Game:
    def __init__(self, interface, num_rows=6, num_columns=7, win_num=4):
        """
        Parameters
        ----------
        interface: CLI
            The interface being used for the game.
        num_rows: int
            The number of rows in the grid.
        num_columns: int
            The number of columns in the grid.
        win_num: int
            The number of symbols in a row needed to win.

        """
        self.interface = interface
        self.num_rows = num_rows
        self.num_columns = num_columns

        self.grid = Grid(num_rows, num_columns, win_num)

        self.symbols: list = ['R', 'B', 'G', 'X']  # The default symbols to use if invalid symbols are given by the
        # Interface

        self.players: list = []  # The players in the game
        self.game_over: bool = False
        self.current_player_num: int = 0  # The index of the player whose turn it is
        self.current_player = None
        self.turn_num: int = 0
        self.past_states: dict = {}  # A dictionary of past game states with the turn num as the index

    def add_human_player(self, name: str, symbol=""):
        """
        Adds a human player to the list of players.
        Parameters
        ----------
        name: str
            The name of the player.
        symbol: str
            The symbol of the player.

        """
        self.players.append(Player(self, name, symbol))

    def add_computer_player(self, name: str, difficulty: int, symbol=""):
        """
        Adds a computer player to the list of players.
        Parameters
        ----------
        name: str
            The name of the player.
        difficulty: int
            The difficulty of the player.
        symbol: str
            The symbol of the player.

        """
        self.players.append(ComputerPlayer(self, name, difficulty, symbol))

    def make_player_move(self):
        """
        Gets a valid move from the player and then makes that move in the grid.

        """
        move_made = False
        while not move_made:
            try:
                # If an index error is raised that means that it is an invalid move (likely because the column is full)
                # so we ask the player to make it again
                move = self.current_player.get_move()
                self.grid.add_piece(move, self.current_player.symbol)
                move_made = True
                self.add_to_past_dict(move)

            except IndexError as error:
                self.current_player.register_error(error)

    def play_game(self):
        """
        Main logic of the game. Loops through the players until the game has ended

        """
        self.current_player = self.players[self.current_player_num]
        self.interface.display_grid()
        while not self.game_over:
            self.make_player_move()

            self.interface.display_grid()
            self.turn_num += 1

            if self.grid.check_win():
                self.game_over = True
                self.interface.display_win(self.current_player)

            elif self.grid.grid_full():
                self.game_over = True
                self.interface.display_draw()

            else:
                self.current_player_num = (self.current_player_num + 1) % len(self.players)
                self.current_player = self.players[self.current_player_num]

    def add_to_past_dict(self, move_made):
        """
        Adds the current grid and the move to the past dictionary.
        Parameters
        ----------
        move_made: int
            The move that the current player has just made.

        """
        if move_made is None:
            self.past_states[self.turn_num] = copy.deepcopy(self.grid), None, None

        else:
            self.past_states[self.turn_num] = copy.deepcopy(self.grid), move_made, self.grid.column_height(
                move_made) - 1

    def evaluate_move(self, move: int):
        # This will look at the dictionary of moves and evaluate the move made on a scale of -10 to 10
        pass


class Player:
    def __init__(self, game: Game, name: str, symbol=""):
        """
        Parameters
        ----------
        game: Game
            The game object.
        name: str
            The name of the player.
        symbol: str
            The symbol of the player.
        """
        self.game = game
        self.name = name
        if symbol == "":
            self.symbol = self.game.symbols.pop()

        else:
            self.symbol = symbol

    def get_move(self):
        """
        Gets the move from the player through the interface
        Returns
        -------
        int
            The move the player has made.

        """
        return self.game.interface.get_move(self)

    def register_error(self, error):
        """
        Notifies the interface that an error has occurred.
        Parameters
        ----------
        error

        """
        self.game.interface.display_invalid_move(error)


class ComputerPlayer(Player):
    # The values to pass into strategy depending on the difficulty.
    difficulty_dict = {0: (0, 0.0),
                       1: (4, 0.5),
                       2: (7, 0.6),
                       3: (10, 0.8),
                       4: (11, 1.0)}

    def __init__(self, game: Game, name: str, difficulty: int, symbol=""):
        super().__init__(game, name, symbol)
        self.difficulty = difficulty
        difficulty_tuple = ComputerPlayer.difficulty_dict[difficulty]
        self.strategy = Strategy(game.grid, self.symbol, difficulty_tuple[0], difficulty_tuple[1])

    def get_move(self):
        """
        Finds and returns the move based on the computer difficulty.
        Returns
        -------
        int
            The move the computer has made

        """
        return self.strategy.move()

    def register_error(self, error):
        raise IndexError("Computer has made an invalid move.")
