import pytest
from main_project import strategy
from main_project.connect4_grid import Grid
import math
import random


class TestEvaluator:
    @pytest.fixture()
    def empty_grid(self):  # Empty Grid
        grid_0 = Grid()

        evaluator = strategy.Evaluator(grid_0, "R", 8)
        evaluator.grid_to_int()

        return evaluator

    @pytest.fixture()
    def full_grid(self):
        grid_1 = Grid()  # Full Grid

        for i in range(grid_1.num_columns):
            for _ in range(grid_1.num_rows):
                grid_1.add_piece(i, "R")

        evaluator = strategy.Evaluator(grid_1, "R", 8)
        evaluator.grid_to_int()

        return evaluator

    @pytest.fixture()
    def evaluator_2(self):
        grid_2 = Grid()  # 1 3-in-a-row.

        for i in range(3):
            grid_2.add_piece(0, "R")

        evaluator = strategy.Evaluator(grid_2, "R", 8)
        evaluator.grid_to_int()

        return evaluator

    @pytest.fixture()
    def evaluator_3(self):
        grid_3 = Grid()  # 2 3-in-a-rows

        for i in range(3):
            grid_3.add_piece(0, "R")
            grid_3.add_piece(1, "B")

        evaluator = strategy.Evaluator(grid_3, "R", 8)
        evaluator.grid_to_int()
        return evaluator

    @pytest.fixture()
    def evaluator_4(self):
        grid_4 = Grid()  # 4 in a row

        for i in range(4):
            grid_4.add_piece(0, "R")

        evaluator = strategy.Evaluator(grid_4, "R", 8)
        evaluator.grid_to_int()
        return evaluator

    @pytest.fixture()
    def evaluators(self, empty_grid, full_grid, evaluator_2, evaluator_3, evaluator_4):
        return [empty_grid, full_grid, evaluator_2, evaluator_3, evaluator_4]

    def test_grid_to_int(self, empty_grid, full_grid, evaluator_2, evaluator_3):
        assert empty_grid._position == 0
        assert empty_grid._mask == 0
        assert full_grid._position == 279258638311359
        assert full_grid._mask == 279258638311359
        assert evaluator_2._position == 30786325577728
        assert evaluator_2._mask == 30786325577728
        assert evaluator_3._position == 30786325577728
        assert evaluator_3._mask == 31026843746304

    def test_check_4_in_a_row(self, evaluators):
        assert not evaluators[0].check_n_in_a_row(evaluators[0]._position)
        assert evaluators[1].check_n_in_a_row(evaluators[1]._position)
        assert not evaluators[2].check_n_in_a_row(evaluators[2]._position)
        assert not evaluators[3].check_n_in_a_row(evaluators[3]._position)
        assert evaluators[4].check_n_in_a_row(evaluators[4]._position)

    def test_make_move(self, evaluators):
        move_0 = evaluators[0].make_move(evaluators[0]._mask, evaluators[0]._position, 6)
        assert move_0[0] == 1
        assert move_0[1] == 0
        assert move_0[2] == 0

    def test_minimax(self, evaluators):
        assert not evaluators[0].evaluate_self()[0]
        assert not evaluators[1].evaluate_self()[0]
        assert evaluators[2].evaluate_self() == (math.inf, 1)
        assert evaluators[3].evaluate_self() == (math.inf, 1)
        assert evaluators[4].evaluate_self() == (math.inf, 1)

    def test_heuristic(self, evaluators):
        assert evaluators[0].evaluate_grid(evaluators[0]._position) == 0
        assert evaluators[1].evaluate_grid(evaluators[1]._position) == 276
        assert evaluators[2].evaluate_grid(evaluators[2]._position) == 12
        assert evaluators[3].evaluate_grid(evaluators[3]._position) == 12
        assert evaluators[4].evaluate_grid(evaluators[4]._position) == 17


class TestStrategy:
    @pytest.fixture()
    def testing_grid(self):
        grid = Grid()
        for i in range(3):
            grid.add_piece(0, "R")

        for i in range(3):
            grid.add_piece(3, "B")

        return grid

    @pytest.fixture()
    def random_strategy(self, testing_grid):
        random_strategy = strategy.Strategy(testing_grid, "R", 5, 0.5)
        return random_strategy

    @pytest.fixture()
    def perfect_strategy(self, testing_grid):
        perfect_strategy = strategy.Strategy(testing_grid, "R", 5, 1.0)
        return perfect_strategy

    def test_strategies(self, random_strategy, perfect_strategy):
        random.seed(0)
        random_strategy.rank_moves()

        random.seed(0)
        perfect_strategy.rank_moves()

        assert random_strategy.ranked_indices == [0, 3, 4, 2, 1, 5, 6]
        assert perfect_strategy.ranked_indices == [0, 3, 4, 2, 1, 5, 6]

        random.seed(1)
        assert random_strategy.move() == 3
        assert perfect_strategy.move() == 0
