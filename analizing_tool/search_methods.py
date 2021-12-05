import ruptures as rpt

import autoregression


def nmr(data, n_breakpoints):
    _, result = autoregression.predict(data, n_breakpoints)
    return result


def ruptures_dynp(data, n_breakpoints):
    algo = rpt.Dynp(model="l1", min_size=1).fit(data)
    result = algo.predict(n_breakpoints)
    result.pop()
    return result


def vempaliakhil(data, n_breakpoints):
    v = vempaliakhil96.cal_cost(data)
    return vempaliakhil96.cal_tau(v, data, n_breakpoints + 1)
