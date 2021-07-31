import csv

import matplotlib.pyplot as plt
import numpy as np


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
