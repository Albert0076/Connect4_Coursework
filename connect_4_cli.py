from back_end import Game, Player
import pyinputplus


class CLI:
    difficulty_dictionary = {"Easy": 1,
                             "Medium": 2,
                             "Hard": 3}

    def __init__(self):
        self.game = None
        self.setup()

    def setup(self):
        print(f'Use default rules? Y/N')
        default_rules = pyinputplus.inputYesNo()
        if not default_rules:
            columns = pyinputplus.inputInt("Enter columns: ", min=1)
            rows = pyinputplus.inputInt("Enter rows: ", min=1)
            win_number = pyinputplus.inputInt("Enter win number: ", min=1)
            self.game = Game(self, rows, columns, win_number)

        else:
            self.game = Game(self)

        for i in range(2):
            self.add_player()

        self.game.play_game()

    def add_player(self):
        print("Add player: ")
        computer_choice = pyinputplus.inputChoice(["Human", "Computer"])
        player_name = pyinputplus.inputStr("Enter player name: ",
                                           blockRegexes=[player.name for player in self.game.players])
        player_symbol = pyinputplus.inputStr("Enter Symbol (must be one letter): ",
                                             limit=1, blockRegexes=[player.symbol for player in self.game.players])
        if computer_choice == "Human":
            self.game.add_human_player(player_name, player_symbol)

        else:
            difficulty = pyinputplus.inputChoice(["Easy", "Medium", "Hard"], "Enter difficulty: ")
            self.game.add_computer_player(player_name, CLI.difficulty_dictionary[difficulty], player_symbol)

    def get_move(self, game: Game, player: Player):
        pass

    def display_win(self, player: Player):
        pass

    def display_grid(self):
        pass

    def display_invalid_move(self, error):
        pass
