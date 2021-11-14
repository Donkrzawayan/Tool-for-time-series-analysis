import ruptures as rpt

from . import autoregression
from . import vempaliakhil96


def nmr(data, n_breakpoints):
    _, result = autoregression.predict(data, n_breakpoints)
    return result


def ruptures(data, n_breakpoints):
    algo = rpt.Dynp(min_size=1).fit(data)
    return algo.predict(n_breakpoints)


def vempaliakhil(data, n_breakpoints):
    v = vempaliakhil96.cal_cost(data)
    return vempaliakhil96.cal_tau(v, data, n_breakpoints + 1)
