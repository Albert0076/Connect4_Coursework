from connect4_structure_prototype import Grid
import random

class Strategy:
    def __init__(self, grid: Grid, player_symbol: str):
        self.symbol = player_symbol
        self.grid = grid


    def move(self):
        pass



class VeryEasy(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)


    def move(self):
        return random.choice([column for column in self.grid.columns if not self.grid.line_full(column)])



class Easy(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)


    def move(self):
        pass


class Medium(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)

    def move(self):
        pass


class Hard(Strategy):
    def __init__(self, grid: Grid, player_symbol: str):
        super().__init__(grid, player_symbol)

    def move(self):
        pass


class Evaluator:
    def __init__(self, grid: Grid, player_symbol: str):
        self.grid = grid
        self.player_symbol = player_symbol


        self._position: int = 0
        self._mask: int = 0




    def grid_to_int(self):
        position = ''
        mask = ''
        for column in range(self.grid.num_columns):
            mask += "0"
            position += "0"
            for row in range(self.grid.num_rows-1, -1, -1):
                mask += ['0', '1'][not self.grid.cells[(row, column)].is_empty()]
                position += ['0', '1'][self.grid.cells[(row, column)].symbol == self.player_symbol]


        self._position = int(position, 2)
        self._mask = int(mask, 2)




    def __repr__(self):
        return Evaluator(grid=self.grid, player_symbol=self.player_symbol)


    def __str__(self):
        mask_str = format(self._mask, f'0{self.grid.num_columns * (self.grid.num_rows+1)}b')
        output_list = [[" " for __ in range(self.grid.num_columns)] for _ in range(self.grid.num_rows+1)]
        i, j = self.grid.num_rows, 0
        for symbol in mask_str:
            i = (i+1) % (self.grid.num_rows+1)
            output_list[i][j] = symbol
            if i == self.grid.num_rows:
                j +=1

        return "".join(["".join(column_list) + "\n" for column_list in output_list])

