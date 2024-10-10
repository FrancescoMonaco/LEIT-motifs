from concurrent.futures import ProcessPoolExecutor, as_completed
import itertools
import numpy as np
import time
from numba import jit

if __name__ == "__main__":

    # Array of random numbers long 1000
    random_numbers = np.random.rand(1000)
    random_numbers2 = np.random.rand(1000)

    init = time.time()
    for i in range(10000):
        f = np.array_equal(random_numbers, random_numbers2)
    print("Time elapsed: ", time.time() - init)
