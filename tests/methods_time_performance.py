import time
import pytest

from analizing_tool import random_time_series as rts
from analizing_tool import search_methods

REPEAT = 60


def test():
    n_data_points, n_breakpoints, snr = 100, 5, 30
    time_series = []

    for _ in range(REPEAT):
        data, _ = rts.gen_rand(n_data_points, n_breakpoints, snr)
        time_series.append(data)

    print()  # new line

    start = time.process_time()
    for data in time_series:
        _ = search_methods.nmr(data, n_breakpoints)
    end = time.process_time()
    print(end - start)

    start = time.process_time()
    for data in time_series:
        _ = search_methods.ruptures_dynp(data, n_breakpoints)
    end = time.process_time()
    print(end - start)

    start = time.process_time()
    for data in time_series:
        _ = search_methods.ruptures_binseg(data, n_breakpoints)
    end = time.process_time()
    print(end - start)

    assert True


if __name__ == '__main__':
    test()
