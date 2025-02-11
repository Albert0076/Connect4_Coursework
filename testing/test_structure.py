import pytest
from main_project.connect4_structure import Grid


class TestGrid:
    @pytest.fixture()
    def empty_grid(self):
        grid = Grid()
        return grid

    @pytest.fixture()
    def full_grid(self):
        grid = Grid()
        for i in range(grid.num_columns):
            for _ in range(grid.num_rows):
                grid.add_piece(i, "R")

        return grid

    @pytest.fixture()
    def three_in_a_row(self):
        grid = Grid()
        for i in range(3):
            grid.add_piece(i, "R")

        return grid

    @pytest.fixture()
    def four_in_a_rows(self):
        grid_h = Grid()
        for i in range(4):
            grid_h.add_piece(i, "R")

        grid_v = Grid()
        for _ in range(4):
            grid_v.add_piece(0, "R")
        # //
        grid_d1 = Grid()
        for i in range(4):
            for _ in range(i):
                grid_d1.add_piece(i, "B")

            grid_d1.add_piece(i, "R")

        # \\
        grid_d2 = Grid()
        for i in range(4):
            for _ in range(3 - i):
                grid_d2.add_piece(i, "B")

            grid_d2.add_piece(i, "R")

        return [grid_h, grid_v, grid_d1, grid_d2]

    def test_add_piece(self, empty_grid):
        for i in range(len(empty_grid.columns)):
            empty_grid.add_piece(i, "R")
            assert empty_grid.cells[(0, i)].symbol == "R"

    def test_grid_full(self, full_grid):
        assert full_grid.grid_full()

    def test_four_in_a_row(self, three_in_a_row, four_in_a_rows):
        assert not three_in_a_row.check_win()
        for grid in four_in_a_rows:
            assert grid.check_win()

    def test_column_height(self, empty_grid, full_grid, three_in_a_row):
        assert empty_grid.column_height(0) == 0
        assert full_grid.column_height(0) == 6
        assert three_in_a_row.column_height(0) == 1



