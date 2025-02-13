from main_project.back_end import Game, Player
import pyinputplus
from colorama import Fore, Style
import math

class Interface:
    # This is the basic template for an interface. All interfaces (CLI or GUI) must have these methods.
    def __init__(self):
        self.game = None

    def setup(self):
        pass

    def get_move(self, player: Player):
        pass

    def display_grid(self):
        pass

    def display_move(self, move: int):
        pass

    def display_win(self, player: Player):
        pass

    def display_draw(self):
        pass

    def display_invalid_move(self, error):
        pass

    def computer_thinking(self, player: Player):
        pass


class CLI(Interface):
    difficulty_dictionary = {"Very Easy": 0,
                             "Easy": 1,
                             "Medium": 2,
                             "Hard": 3,
                             "Perfect": 4}

    colours = {"R": Fore.RED, "B": Fore.BLUE, "G": Fore.GREEN, "Y": Fore.YELLOW, }

    def __init__(self):
        super().__init__()
        self.game = None
        self.symbols = [key for key in CLI.colours.keys()]

    def setup(self):
        """
        Initialises the game and gets the ruleset.

        """
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

    def comp_v_comp(self):
        self.game = Game(self)
        self.game.add_computer_player("Hal 9000", 4, "R")
        self.game.add_computer_player("C3PO", 4, "B")

        self.game.play_game()
        self.analyse_game()

    def comp_v_human(self):
        self.game = Game(self)
        self.game.add_human_player("Raiden", "R")
        self.game.add_computer_player("Arsenal Gear", 4, "B")

        self.game.play_game()
        self.analyse_game()

    def human_v_human(self):
        self.game = Game(self)
        self.game.add_human_player("Harry", "R")
        self.game.add_human_player("Kim", "B")

        self.game.play_game()
        self.analyse_game()

    def add_player(self):
        """
        Adds a player to the game.

        """
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
        """
        Gets a move from the user.
        Parameters
        ----------
        player: Player
            The player who is making the move.

        Returns
        -------
        int
            The move the player has made.

        """
        print(f"Turn {self.game.turn_num}")
        return pyinputplus.inputInt(f"Player: {player.name}, enter column: ", min=1, max=self.game.num_columns) - 1

    def computer_thinking(self, player: Player):
        """
        Shows that a computer player is calculating the next move.
        Parameters
        ----------
        player: Player
            The computer player who is calculating the next move.

        """
        print(f"Turn {self.game.turn_num}")
        print(f"Computer Player {player.name} is thinking.")

    def display_win(self, player: Player):
        """
        Shows that a player has won the game.
        Parameters
        ----------
        player: Player
            The player who was won the game.

        """
        print(f"Player: {player.name} has won the game!")
        print(f"The game took {self.game.turn_num} turns.")

    def display_draw(self):
        """
        Displays the game has resulted in a draw.
        """
        print("The Grid is full and the game has ended in a draw")

    def display_grid(self, grid=None, highlighted_moves=None):
        """
        Displays the grid to the player. Allows for specific cells to be highlighted.
        Parameters
        ----------
        grid: Grid
            The grid to be displayed

        highlighted_moves: list[tuple(int, int)]
            The cells to be highlighted
        """
        if highlighted_moves is None:
            highlighted_moves = []
        if grid is None:
            grid = self.game.grid

        return_str = ""
        for row in range(len(grid.rows) - 1, -1, -1):
            for cell in grid.rows[row]:
                if grid.cells[cell].is_empty():
                    return_str += "|_| "

                else:
                    bright = ""
                    for move in highlighted_moves:
                        if cell == move:
                            bright = Style.BRIGHT

                    symbol = grid.cells[cell].symbol
                    return_str += "|" + CLI.colours[symbol] + bright + symbol[0] + Style.RESET_ALL + Fore.RESET + "| "

            return_str += "\n"

        for i in range(len(grid.columns)):
            return_str += f" {i + 1}  "

        print(return_str)

    def display_move(self, move):
        """
        Displays the move that has just been made.
        Parameters
        ----------
        move: int
            The move which was just made.

        """
        print(f"{self.game.current_player.name} made the move: {move + 1}.")

    def analyse_game(self):
        """
        Allows the user to analyse the game once it has ended.
        """

        player_choice = pyinputplus.inputYesNo("Do you want to analyse game. Y/N") == "yes"
        while player_choice:
            turn_choice = pyinputplus.inputInt("What turn do you want to look at: ", min=1, max=self.game.turn_num)
            turn = self.game.past_states[turn_choice - 1]
            player_moved = self.game.players[(turn_choice-2) % len(self.game.players)]
            player_to_move = self.game.players[(turn_choice-1) % len(self.game.players)]

            if turn_choice != 1:
                print(f"{player_moved.name} made the move {turn[1]+1}.")

            print(f"It was {player_to_move.name}'s turn.")

            self.display_grid(grid=turn[0], highlighted_moves=[(turn[2], turn[1])])

            evaluate_choice = pyinputplus.inputYesNo("Do you want to evaluate the next move. Y/N") == "yes"
            if evaluate_choice:
                # This functions tells us what symbol to use base on the given value
                # 10: "++", 0 -> 10: "+" , 0: "=", -9 -> -1 : "-", -10: "--"
                evaluate_symbol = lambda x: "!" if x is None else "=" if x == 0 else (
                    ("++" if x == math.inf else "+") if x > 0 else ("--" if x == -math.inf else "-"))

                move_values = self.game.evaluate_move(turn_choice - 1)
                for i in range(len(move_values)):
                    print(f"Move {i + 1}: {evaluate_symbol(move_values[i])}")

            player_choice = pyinputplus.inputYesNo("Do you want to analyse a different turn. Y/N") == "yes"

    def display_score_graph(self):
        evaluated_game = self.game.evaluate_game()
        player_colours = {False: CLI.colours[self.game.players[1].symbol],
                          True: CLI.colours[self.game.players[0].symbol]}

        # 5+ -> 5, (-4, 4) -> (-4, 4), -5- -> -5
        squish_data  = lambda x: 5 if x >= 5 else -5 if x <= -5 else x # Squished the data to the range we want
        cell_full = lambda cell_height, value: ((abs(cell_height) <= abs(squish_data(value))) and
                                                not (cell_height > 0 ^ value > 0))  # Checks if a cell should be coloured
        cell_colour = lambda value: player_colours[value > 0]
        cells = [[cell_full(height, evaluated_game[turn]) * (cell_colour(evaluated_game[turn]) + "#" + Fore.RESET) for turn in range(self.game.turn_num)]
                 for height in range(5, -6, -1)]





    def display_invalid_move(self, error):
        """
        Display an invalid move
        Parameters
        ----------
        error:
            The error message resulting from the invalid move.
        """
        print(f"That is an invalid move: {error}.")


if __name__ == "__main__":
    cli = CLI()
    cli.comp_v_comp()

