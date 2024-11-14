# A lot of the work on this file is taken from this article:
# https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
from connect4_structure_prototype import Grid

# The Grid will be represented by an 8x8 grid with the top row being always empty, it will be represented by 8 8bit binary numbers with each byte representing a column

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


def print_grid(grid_int):
    grid_str = format(grid_int, '049b')
    out_str = [[" " for j in range(7)] + ["\n"] for i in range(6, -1, -1)]
    i, j = 6, 6
    for symbol in grid_str:
        out_str[i][j] = symbol
        i = (i+1) % 7
        if i == 6:
            j -= 1

    return "".join(["".join(str_list) for str_list in out_str[::-1]])





def check_four_in_a_row(position):
    # Check Horizontal:
    # & - Bitwise And, | - Bitwise Or, ^ - Bitwise XOR, >> - shift bits to the left
    shift = position & (position >> 7)
    if shift & (shift >> 14):
        return True


    # Diagonal \
    shift = position & (position >> 6)
    if shift & (shift >> 12):
        return True

    # Diagonal /
    shift = position & (position >> 8)
    if shift & (shift >> 16):
        return True

    # Vertical
    shift = position & (position >> 1)
    if shift & (shift >> 2):
        return True

    return False

def make_move(position, mask, column):
    new_position = position ^ mask # The new position will be the opponent's position which we get from doing an XOR
    v = print_grid((1 << (column*7)))
    u = print_grid(mask +(1 << (column*7)))
    # mask + (1 << (column*7)) will give an empty grid with 1 piece in the column, adding this to the mask will carry the bit until it is at the top of the column
    new_mask = mask | (mask + (1 << (column * 7)))
    return new_position, new_mask








if __name__ == "__main__":
    grid = Grid()
    for i in range(4):
        for j in range(i):
            grid.add_piece(i, "Y")

        grid.add_piece(i, "R")

    b_grid = get_bit_mask(grid, "Y")
    print(b_grid)
    out_grid = make_move(b_grid[0], b_grid[1], 5)
    print(print_grid(b_grid[0]) + "\n" +  print_grid(out_grid[0]))
    print(print_grid(b_grid[1]) + "\n" + print_grid(out_grid[1]))

