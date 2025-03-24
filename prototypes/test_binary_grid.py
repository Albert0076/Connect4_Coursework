import pytest
from prototypes.binary_string_minimax_test import get_bit_mask, check_four_in_a_row
from main_project.connect4_grid import Grid

class TestBinaryGrid:
    @pytest.fixture()
    def vertical(self, n):
        grid = Grid()
        for i in range(n):
            grid.add_piece(0, "R")

        return get_bit_mask(grid, "R")

    @pytest.fixture()
    def horizontal(self, n):
        grid = Grid()
        for i in range(n):
            grid.add_piece(i, "R")

        return get_bit_mask(grid, "R")

    @pytest.fixture()
    def diagonal1(self, n):
        grid = Grid()
        for i in range(n):
            for j in range(i):
                grid.add_piece(i, "Y")

            grid.add_piece(i, "R")

        return get_bit_mask(grid, "R")

    @pytest.fixture()
    def diagonal2(self, n):
        grid = Grid()
        for i in range(n):
            for j in range(n-i-1):
                grid.add_piece(i, "Y")

            grid.add_piece(i, "R")

        return get_bit_mask(grid, "R")


    @pytest.mark.parametrize('vertical, horizontal, diagonal1, diagonal2', [], )
    def assert_three_in_a_row(self, vertical, horizontal, diagonal1, diagonal2):
        assert not check_four_in_a_row(vertical) == True
        assert not check_four_in_a_row(horizontal) == True
        assert not check_four_in_a_row(diagonal1) == True
        assert not check_four_in_a_row(diagonal2) == True

    @pytest.mark.parametrize('vertical, horizontal, diagonal1, diagonal2', [4, 4, 4, 4], indirect=True)
    def assert_four_in_a_row(self, vertical, horizontal, diagonal1, diagonal2):
        assert check_four_in_a_row(vertical) == True
        assert check_four_in_a_row(horizontal) == True
        assert check_four_in_a_row(diagonal1) == True
        assert check_four_in_a_row(diagonal2) == True


if __name__ == '__main__':
    test = TestBinaryGrid()
    test.assert_three_in_a_row()
    test.assert_four_in_a_row()

