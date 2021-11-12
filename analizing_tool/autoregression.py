import numpy as np


def predict(data, k_gr):
    """Calculates change points by use of dynamic programming

    [1] Michał Staniszewski, Agnieszka Skorupa, Łukasz Boguszewicz, Maria Sokół and Andrzej Polański. Quality Control Procedure Based on Partitioning of NMR Time Series.

    :param data: array
    :param k_gr: number of change points
    :return:
        opt_part: sorted list of breakpoints
    """
    q = np.zeros(k_gr)
    n = len(data)
    p_opt_idx = np.zeros(n)
    p_aux = np.zeros(n)
    opt_pals = np.zeros((k_gr, n), dtype=int)

    for kk in range(n):
        p_opt_idx[kk] = _cost(data[kk:n])

    # iterate
    for k_ster in range(k_gr):
        for kk in range(n - k_ster - 1):
            for jj in range(kk + 1, n - k_ster):
                p_aux[jj] = _cost(data[kk:jj]) + p_opt_idx[jj]
            ix0, ix1 = kk + 1, n - k_ster
            min_index = np.argmin(p_aux[ix0:ix1])
            mm = p_aux[ix0 + min_index]
            p_opt_idx[kk] = mm
            opt_pals[k_ster, kk] = kk + min_index + 1
        q[k_ster] = p_opt_idx[0]

    # restore optimal decisions
    opt_part = np.zeros((k_gr, k_gr), dtype=int)
    for i in range(k_gr):
        opt_part[i, 0] = opt_pals[i, 0]
        for k_ster in range(i - 1, -1, -1):
            y = opt_part[i, i - k_ster - 1]
            temp = opt_pals[k_ster, y]
            opt_part[i, i - k_ster] = temp

    return q, opt_part[k_gr - 1]


def _cost(vector):
    """Calculate cost according to scoring function in given list"""
    return np.sum(np.abs(vector - np.mean(vector)))
