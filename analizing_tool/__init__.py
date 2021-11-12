import csv

import matplotlib.pyplot as plt
import ruptures as rpt

from . import autoregression
from .random_time_series import gen_rand


def fun():
    x = []
    y = []

    with open(r'datasets/rand_set.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')
        for row in plots:
            x.append(row[0])
            y.append(row[1])

    plt.plot(x, y, label='Loaded from file!')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph')
    plt.legend()
    plt.show()


def ar():
    data_points, n_breakpoints, snr = 100, 5, 30
    data, breakpoints = gen_rand(data_points, n_breakpoints, snr)

    _, result = autoregression.predict(data, n_breakpoints)

    rpt.display(data, breakpoints, result)
    plt.show()


def ruptures():
    data_points, n_breakpoints, snr = 100, 5, 30
    data, breakpoints = gen_rand(data_points, n_breakpoints, snr)

    algo = rpt.Pelt(model="rbf").fit(data)
    result = algo.predict(pen=10)

    rpt.display(data, breakpoints, result)
    plt.show()
