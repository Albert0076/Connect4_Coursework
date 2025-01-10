import pytest
from strategy import Strategy, Evaluator
from connect4_structure_prototype import Grid


class TestEvaluator:
    @pytest.fixture()
    def evaluator_0(self): # Empty Grid
        grid_0 = Grid()

        evaluator = Evaluator(grid_0, "R", 10)
        evaluator.grid_to_int()

        return evaluator


    @pytest.fixture()
    def evaluator_1(self):
        grid_1 = Grid()  # Full Grid

        for i in range(grid_1.num_columns):
            for _ in range(grid_1.num_rows):
                grid_1.add_piece(i, "R")

        evaluator = Evaluator(grid_1, "R", 10)
        evaluator.grid_to_int()

        return evaluator


    @pytest.fixture()
    def evaluator_2(self):
        grid_2 = Grid()  # 1 3-in-a-row.

        for i in range(3):
            grid_2.add_piece(0, "R")

        evaluator = Evaluator(grid_2, "R", 10)
        evaluator.grid_to_int()

        return evaluator

    @pytest.fixture()
    def evaluator_3(self):
        grid_3 = Grid()  # 2 3-in-a-rows

        for i in range(3):
            grid_3.add_piece(0, "R")
            grid_3.add_piece(1, "B")

        evaluator = Evaluator(grid_3, "R", 10)
        evaluator.grid_to_int()
        return evaluator

    @pytest.fixture()
    def evaluator_4(self):
        grid_4 = Grid()

        for i in range(4):
            grid_4.add_piece(0, "R")

        evaluator = Evaluator(grid_4, "R", 10)
        evaluator.grid_to_int()
        return evaluator

    @pytest.fixture()
    def evaluators(self, evaluator_0, evaluator_1, evaluator_2, evaluator_3, evaluator_4):
        return [evaluator_0, evaluator_1, evaluator_2, evaluator_3, evaluator_4]


    def test_grid_to_int(self, evaluator_0, evaluator_1, evaluator_2, evaluator_3):
        assert evaluator_0._position == 0
        assert evaluator_0._mask == 0
        assert evaluator_1._position == 279258638311359
        assert evaluator_1._mask == 279258638311359
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




