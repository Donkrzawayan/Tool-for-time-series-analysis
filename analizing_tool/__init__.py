import csv

import numpy as np
import ruptures as rpt
from matplotlib import pyplot as plt

from . import random_time_series as rts
from . import search_methods


def fun():
    data_points, n_breakpoints, snr = 100, 5, 30
    data, breakpoints = gen_rand(data_points, n_breakpoints, snr)
    data = csv_reading('datasets/Binance_ADAUSDT_d.csv', 3)
    result = search_methods.nmr(data, n_breakpoints)
    rpt.display(data, breakpoints, result)

    plt.show()


def csv_reading(filename, n_row):
    points = []

    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        for row in reader:
            point = float(row[n_row])
            points.append(point)

    return np.array(points)


def gen_rand(data_points=100, n_breakpoints=5, snr=30):
    return rts.gen_rand(data_points, n_breakpoints, snr)
