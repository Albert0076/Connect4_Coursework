import numpy as np
import numpy_testing
from main_project.connect4_grid import Grid
import time

N = 10_000
arrays_np = [np.random.randint(3, size=(6, 7)) for i in range(N)]
arrays_old = [numpy_testing.np_to_grid(grid) for grid in arrays_np]

time_0 = time.time()

fft_arrays = [numpy_testing.check_win(array, 1, 2) for array in arrays_np]

fft_time = time.time() - time_0

time_1 = time.time()

old_values = [grid.check_win() for grid in arrays_old]

old_time = time.time() - time_1



print(fft_time)

print(old_time)
