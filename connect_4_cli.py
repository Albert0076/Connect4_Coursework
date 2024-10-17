from back_end import Game, Player
import pyinputplus

class CLI:
    def __init__(self):
        pass

    def setup(self):
        print(f'Use default rules? Y/N')
        default_rules = pyinputplus.inputYesNo()
        if not default_rules:
            columns = pyinputplus.inputInt("Enter columns: ")

    def get_move(self, game: Game, player: Player):
        pass

    def display_win(self, player: Player):
        pass
