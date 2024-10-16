from connect4_structure_prototype import Grid
from connect_4_cli import CLI


class Game:
    def __init__(self, cli, num_rows=6, num_columns=7, win_num=4):
        self.interface = cli
        self.grid = Grid(num_rows, num_columns, win_num)
        self.symbols = ['R', 'B', 'G', 'X']
        self.players = []
        self.game_over = False
        self.current_player_num: int = 0

    def add_human_player(self, name: str, symbol=""):
        self.players.append(Player(self, name, symbol))

    def add_computer_player(self, name: str, difficulty: int, symbol=""):
        self.players.append(ComputerPlayer(self, name, difficulty, symbol))

    def play_game(self):
        while not self.game_over:
            current_player = self.players[self.current_player_num]
            if not isinstance(current_player, ComputerPlayer):
                move_made = False
                while not move_made:
                    try:
                        self.grid.add_piece(self.interface.get_move(self, current_player), current_player.symbol)
                        move_made = True
                    except IndexError as error:
                        self.interface.display_invalid_move(error)

            else:
                self.grid.add_piece(current_player.get_move(), current_player.symbol)

            self.interface.display_grid()

            if self.grid.check_win():
                self.game_over = True
                self.interface.display_win(current_player)

            else:
                self.current_player_num = (self.current_player_num + 1) % len(self.players)


class Player:
    def __init__(self, game: Game, name: str, symbol=""):
        self.game = game
        self.name = name
        if symbol == "":
            self.symbol = self.game.symbols.pop()

        else:
            self.symbol = symbol


class ComputerPlayer(Player):
    def __init__(self, game: Game, name: str, difficulty: int, symbol=""):
        super().__init__(game, name, symbol)
        self.difficulty = difficulty

    def get_move(self):
        pass
