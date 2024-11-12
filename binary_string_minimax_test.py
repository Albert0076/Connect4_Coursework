# A lot of the work on this file is taken from this article:
# https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
from connect4_structure_prototype import Grid


def get_bit_mask(grid: Grid, player):
    position, mask = '', ''
    for j in range(6, -1, -1):
        # We add an extra row at the top to store the board as 2 64-bit binary numbers
        mask += '0'
        position += '0'
        for i in range(0, 6):
            mask += ['0', '1'][not grid.cells[(i, j)].is_empty()]
            position += ['0', '1'][grid.cells[(i, j)].symbol == player]

    return int(position, 2), int(mask, 2)


def check_four_in_a_row(position):
    # Check Horizontal:
    shift_1 = position & (position >> 7)
    if shift_1 & (shift_1 >> 14):
        return True


if __name__ == "__main__":
    grid = Grid()
    for i in range(4):
        for j in range(i):
            grid.add_piece(i, "Y")

        grid.add_piece(i, "R")

    print(get_bit_mask(grid, "Y"))
    print(grid)
