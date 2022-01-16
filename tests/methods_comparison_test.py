import csv
import pytest

from analizing_tool import random_time_series as rts
from analizing_tool import search_methods


def test():
    data_points, n_breakpoints, snr = 100, 5, 30

    with open('file.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for _ in range(10):
            data, breakpoints = rts.gen_rand(data_points, n_breakpoints, snr)

            nmr = search_methods.nmr(data, n_breakpoints)
            dynp = search_methods.ruptures_dynp(data, n_breakpoints)
            binseg = search_methods.ruptures_binseg(data, n_breakpoints)

            row = []
            row.extend(breakpoints[1:-1])
            row.append(None)
            row.extend(nmr)
            row.append(None)
            row.extend(dynp)
            row.append(None)
            row.extend(binseg)

            writer.writerow(row)

    assert True


if __name__ == '__main__':
    test()
