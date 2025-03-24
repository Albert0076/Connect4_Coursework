from connect4_grid import Grid
import copy
from main_project.strategy import Strategy, Evaluator


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
        self.turn_num: int = 1  # Start at 1 since it is the state after the move has been made
        self.past_states: dict = {0: [copy.deepcopy(self.grid), None,
                                      None]}  # A dictionary of past game states with the turn num as the index
        # {turn_num: [grid, move_made_row, move_made_column]}
        # Turn 0 is an empty grid
        # Turn 1 is after p1 has made a move

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

                return move

            except IndexError as error:
                self.current_player.register_error(error)

    def play_game(self):
        """
        Main logic of the game. Loops through the players until the game has ended

        """
        self.current_player = self.players[self.current_player_num]
        self.interface.display_grid()
        while not self.game_over:
            move = self.make_player_move()  # Want to send the CLI the move

            self.interface.display_grid(highlighted_moves=[(self.grid.column_height(move) - 1, move)])
            self.interface.display_move(move)

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

    def evaluate_move(self, turn: int, depth=11):
        """
        Evaluates the grid at the given turn, returning the evaluators value for each move that could have been made.
        Parameters
        ----------
        turn: int
            The turn to check.
        depth: int
            The depth at which the evaluator will check.

        Returns
        -------
        list[int]
            The evaluators values for all the possible moves.

        """
        # This will look at the dictionary of moves and evaluate the move made on a scale of -10 to 10
        # If it is turn 5 and red has just made a move then it will evaluate the possible moves for blue.
        evaluator = Evaluator(self.past_states[turn][0], self.players[turn % len(self.players)].symbol, depth)
        evaluator.grid_to_int()
        evaluator.calculate_move_values()
        # Need to check if it is a none value.
        return [element if element is None else element[0] for element in evaluator.move_values]


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
                       1: (3, 0.7),
                       2: (6, 0.8),
                       3: (9, 0.95),
                       4: (10, 1.0)}

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
        self.game.interface.computer_thinking(self)

        return self.strategy.move()

    def register_error(self, error):
        raise IndexError("Computer has made an invalid move.")
