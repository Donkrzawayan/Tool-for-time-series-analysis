import ruptures as rpt

from . import autoregression


def nmr(data, n_breakpoints):
    _, result = autoregression.predict(data, n_breakpoints)
    return result


def ruptures_dynp(data, n_breakpoints):
    algo = rpt.Dynp(model="l1", min_size=1).fit(data)
    result = algo.predict(n_breakpoints)
    result.pop()
    return result


def ruptures_binseg(data, n_breakpoints):
    algo = rpt.Binseg(model="l1", min_size=1).fit(data)
    result = algo.predict(n_breakpoints)
    result.pop()
    return result
