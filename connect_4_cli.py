from back_end import Game, Player
import pyinputplus
from colorama import Fore, Style


class CLI:
    difficulty_dictionary = {"Very Easy": 0,
                             "Easy": 1,
                             "Medium": 2,
                             "Hard": 3, }

    colours = {"R": Fore.RED, "B": Fore.BLUE, "G": Fore.GREEN, "Y": Fore.YELLOW, }

    def __init__(self):
        self.game = None
        self.symbols = [key for key in CLI.colours.keys()]

        self.setup()

    def setup(self):
        print(f'Use default rules? Y/N')
        default_rules = pyinputplus.inputYesNo() == "yes"
        if not default_rules:
            columns = pyinputplus.inputInt("Enter columns: ", min=1)
            rows = pyinputplus.inputInt("Enter rows: ", min=1)
            win_number = pyinputplus.inputInt("Enter win number: ", min=1)
            self.game = Game(self, rows, columns, win_number)

        else:
            self.game = Game(self)

        for _ in range(2):
            self.add_player()

        self.game.play_game()
        self.analyse_game()

    def add_player(self):
        print("Add player: ")
        computer_choice = pyinputplus.inputChoice(["Human", "Computer"])
        player_name = pyinputplus.inputStr("Enter player name: ",
                                           blockRegexes=[player.name for player in self.game.players])
        print("Enter Symbol: ")
        player_symbol = pyinputplus.inputChoice(self.symbols)
        self.symbols.remove(player_symbol)
        if computer_choice == "Human":
            self.game.add_human_player(player_name, player_symbol)

        else:
            print("Choose Difficulty: ")
            difficulty = pyinputplus.inputChoice([key for key in CLI.difficulty_dictionary.keys()])
            self.game.add_computer_player(player_name, CLI.difficulty_dictionary[difficulty], player_symbol)

    def get_move(self, player: Player):
        return pyinputplus.inputInt(f"Player: {player.name}, enter column: ", min=1, max=self.game.num_columns) - 1

    def display_win(self, player: Player):
        print(f"Player: {player.name} has won the game!")
        print(f"The game took {self.game.turn_num} turns.")

    def display_grid(self, grid=None, highlighted_moves=None):
        if highlighted_moves is None:
            highlighted_moves = []
        if grid is None:
            grid = self.game.grid

        return_str = ""
        for i in range(len(grid.rows) - 1, -1, -1):
            for cell in grid.rows[i]:
                if grid.cells[cell].is_empty():
                    return_str += "|_| "

                else:
                    bright = ""
                    for move in highlighted_moves:
                        if cell == move:
                            bright = Style.BRIGHT

                    symbol = grid.cells[cell].symbol
                    return_str += "|" + CLI.colours[symbol] + bright + grid.cells[cell].symbol[
                        0] + Style.RESET_ALL + Fore.RESET + "| "

            return_str += "\n"

        for i in range(len(grid.columns)):
            return_str += f" {i + 1}  "

        print(return_str)

    def analyse_game(self):
        player_choice = pyinputplus.inputYesNo("Do you want to analyse game. Y/N") == "yes"
        while player_choice:
            turn_choice = pyinputplus.inputInt("What turn do you want to look at: ", min=1, max=self.game.turn_num)
            turn = self.game.past_states[turn_choice - 1]
            self.display_grid(grid=turn[0], highlighted_moves=[(turn[2], turn[1])])
            player_choice = pyinputplus.inputYesNo("Do you want to analyse a different turn. Y/N") == "yes"

    @staticmethod
    def display_invalid_move(error):
        print(f"That is an invalid move: {error}.")


if __name__ == "__main__":
    cli = CLI()
