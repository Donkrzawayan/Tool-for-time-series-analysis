import numpy as np


def cal_cost(y):
    n = len(y)
    V = np.full([n, n], np.inf)
    for j1 in range(n):
        for j2 in range(j1, n, 1):
            yj = y[j1:j2]
            yj_mean = float(np.mean(yj))
            V[j1, j2] = np.sum((yj-yj_mean)**2)
    return V


def cal_tau(V, y, Kmax):
    """Calculate breakpoints (taus) given the cost function matrix"""
    U = np.zeros(Kmax)
    Nr = Kmax - 1
    n = len(y)
    U[0] = V[0, -1].copy()
    D = V[:, -1].copy()
    Pos = np.full([n, Nr], np.inf)
    Pos = Pos.astype(int)
    Pos[-1, :] = np.array([n]*Nr)
    tau_mat = np.full([Nr, Nr], np.inf)
    tau_mat = tau_mat.astype(int)
    for k in range(1, Nr+1, 1):
        for j in range(n-1):
            dist = V[j, j:n-1] + D[j+1:n]
            D[j] = min(dist)
            Pos[j, 0] = np.argmin(dist) + j
            if k > 1:
                Pos[j, 1:k] = Pos[Pos[j, 0], :(k-1)]
        U[k] = D[0]
        tau_mat[k-1, 0:k+1] = Pos[0, 0:k+1]
    return tau_mat[-1, :]