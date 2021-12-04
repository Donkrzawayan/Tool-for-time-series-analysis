import numpy as np


def gen_rand(n_data_points, n_change_points, snr, repeat=1):
    """Generates random time series, distorted by white noise, which is based on randomly generated change points

    Returns:
        result: array.
        change_points: list of change point indexes.
    """
    offset = 10
    cp_range = range(offset, n_data_points - offset)
    change_points = np.sort(np.random.choice(cp_range, n_change_points, replace=False))
    change_points = np.r_[0, change_points, n_data_points - 1]  # 0 to first, n_data_points - 1 to last position
    result = np.zeros((n_data_points - 1, repeat))
    segments = np.random.rand(repeat, n_change_points + 1)

    for i in range(repeat):
        data = []

        for j in range(n_change_points + 1):
            probe = np.full(change_points[j + 1] - change_points[j], segments[i, j])
            data = np.append(data, probe)

        data = data + _awgn(data, snr)
        result[:, i] = data

    return result, change_points


def _awgn(data, snr):
    """Additive white Gaussian noise"""
    snr = 10 ** (snr / 10.0)
    x_power = np.sum(data ** 2) / len(data)
    n_power = x_power / snr
    return np.random.randn(len(data)) * np.sqrt(n_power)
