import csv

import matplotlib.pyplot as plt

import analizing_tool.random_time_series as rts


def conv(x):
    return x.replace(',', '.').encode()


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


def gen_rand():
    data_points = 100
    change_points = 5
    snr = 30
    data, _ = rts.gen_rand(data_points, change_points, snr)
    plt.plot(data)
    plt.show()
