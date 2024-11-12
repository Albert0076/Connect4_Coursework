from connect4_structure_prototype import Grid
import copy
import random


class Game:
    def __init__(self, cli, num_rows=6, num_columns=7, win_num=4):
        self.interface = cli
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.grid = Grid(num_rows, num_columns, win_num)
        self.symbols = ['R', 'B', 'G', 'X']
        self.players = []
        self.game_over = False
        self.current_player_num: int = 0
        self.turn_num = 0
        self.past_states = {}

    def add_human_player(self, name: str, symbol=""):
        self.players.append(Player(self, name, symbol))

    def add_computer_player(self, name: str, difficulty: int, symbol=""):
        self.players.append(ComputerPlayer(self, name, difficulty, symbol))

    def play_game(self):
        self.interface.display_grid()
        self.add_to_past_dict(None)
        while not self.game_over:
            current_player = self.players[self.current_player_num]
            move_made = False
            move = None
            while not move_made:
                try:
                    move = current_player.get_move()
                    self.grid.add_piece(move, current_player.symbol)
                    move_made = True
                    self.add_to_past_dict(move)

                except IndexError as error:
                    current_player.register_error(error)

            self.interface.display_grid()
            self.turn_num += 1
            if self.grid.check_win():
                self.game_over = True
                self.interface.display_win(current_player)

            else:
                self.current_player_num = (self.current_player_num + 1) % len(self.players)

    def add_to_past_dict(self, move_made):
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
        self.game = game
        self.name = name
        if symbol == "":
            self.symbol = self.game.symbols.pop()

        else:
            self.symbol = symbol

    def get_move(self):
        return self.game.interface.get_move(self)

    def register_error(self, error):
        self.game.interface.display_invalid_move(error)


class ComputerPlayer(Player):
    def __init__(self, game: Game, name: str, difficulty: int, symbol=""):
        super().__init__(game, name, symbol)
        self.difficulty = difficulty

    def get_move(self):
        if self.difficulty == 0:
            return self.very_easy()

        return 0

    def very_easy(self):
        return random.randint(0, self.game.num_columns - 1)

    def register_error(self, error):
        pass
