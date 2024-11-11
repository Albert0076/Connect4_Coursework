# A lot of the work on this file is taken from this article:
# https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
from connect4_structure_prototype import Grid

def get_bit_mask(grid: Grid, player):
    position, mask = '', ''
    for j in range(6, -1, -1):
        mask += '0'
        position += '0'
        for i in range(0, 6):
            mask += ['0', '1'][grid.cells[(i, j)].isempty()]
            position += ['0', '1'][grid.cells[(i, j)].symbol == player]



