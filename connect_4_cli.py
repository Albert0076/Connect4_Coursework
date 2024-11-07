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
        default_rules = pyinputplus.inputYesNo() == "Y"
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
        self.analyse_game()

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
        return pyinputplus.inputInt(f"Player: {player.name}, enter column: ", min=1, max=self.game.num_columns) - 1

    def display_win(self, player: Player):
        print(f"Player: {player.name} has won the game!")
        print(f"The game took {self.game.turn_num} turns.")

    def display_grid(self):
        print(self.game.grid)

    def analyse_game(self):
        player_choice = pyinputplus.inputYesNo("Do you want to analyse game. Y/N")
        while player_choice:
            turn_choice = pyinputplus.inputInt("What turn do you want to look at: ", min=0, max=self.game.turn_num)




    @staticmethod
    def display_invalid_move(error):
        print(f"That is an invalid move: {error}.")


if __name__ == "__main__":
    cli = CLI()
