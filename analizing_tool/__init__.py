import csv

import numpy as np
import plotly.express as px

from . import random_time_series as rts
from . import search_methods


def fun():
    data_points, n_breakpoints, snr = 100, 5, 30
    data, breakpoints = rts.gen_rand(data_points, n_breakpoints, snr)
    data = csv_reading('datasets/weather_POLAND_ME_US.csv', 8)
    result = search_methods.nmr(data, n_breakpoints)
    # rpt.display(data, breakpoints, result)

    fig = px.line(data, title='Tool for time series analysis')
    for i in range(0, n_breakpoints, 2):
        fig.add_vrect(breakpoints[i], breakpoints[i+1], line_width=0, fillcolor="red", opacity=0.15)
    for breakpoint in result:
        fig.add_vline(breakpoint)
    fig.show()
    # plt.show()


def csv_reading(filename, n_row):
    points = []

    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        for row in reader:
            point = float(row[n_row])
            points.append(point)

    return np.array(points)
