import numpy as np
from connect4_structure_prototype import Grid, Cell
from scipy import signal
import numpy_testing
import time

N = 10_000
arrays = [np.random.randint(3, size=(100, 100)) for i in range(N)]

time_0 = time.time()

fft_arrays = [numpy_testing.check_win_fft(array, 1, 2) for array in arrays]

fft_time = time.time() - time_0

time_1 = time.time()

conv_2d_arrays = [numpy_testing.check_win_2d_conv(array, 1, 2) for array in arrays]

conv_2d_time = time.time() - time_1

time_2 = time.time()

old_arrays = [numpy_testing.old_check_win(array, 1) for array in arrays]

old_time = time.time() - time_2


print(f"FFT Convolution: {fft_time/N:.6f}\n2D Convolution: {conv_2d_time/N:.6f}\nOld Method: {old_time/N:.6f}")