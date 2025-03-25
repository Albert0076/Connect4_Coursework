import pytest
from main_project.back_end import Game, Player, ComputerPlayer
from main_project.connect_4_cli import Interface
from main_project.connect4_grid import Grid

class TestGame:
    @pytest.fixture()
    def default_game(self):
        return Game(Interface())

    @pytest.fixture()
    def winning_game(self):
        game = Game(Interface())
        game.add_computer_player("WALL-E", 5, "B")
        game.add_human_player("Albert", "R")

        for i in range(3):
            game.grid.add_piece(0, "B")

        return game


    def test_add_player(self, default_game):
        default_game.add_human_player("Albert", "R")
        default_game.add_computer_player("WALL-E", 5, "B")

        assert default_game.players[0].name == "Albert"
        assert default_game.players[0].symbol == "R"
        assert default_game.players[1].name == "WALL-E"
        assert default_game.players[1].difficulty == 5
        assert default_game.players[1].symbol == "B"

    def test_computer_player(self, winning_game):
        assert winning_game.players[0].get_move() == 0


