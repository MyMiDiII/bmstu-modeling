from prettytable import PrettyTable
import numpy as np

XMAX = 2
STEP = 1e-4
TABLESTEP = 5e-2
NUM = int(TABLESTEP / STEP)


def picard1st(x):
    return x ** 3 / 3


def picard2nd(x):
    return x ** 3 / 3 + x ** 7 / 63


def picard3d(x):
    return (x ** 3 / 3 + x ** 7 / 63
            + 2 * x ** 11 / 2079  + x ** 15 / 59535)


def picard4th(x):
    return (x ** 3 / 3 + x ** 7 / 63
            + 2 * x ** 11 / 2079  + 13 * x ** 15 / 218295 
            + 82 * x ** 19 / 37328445 + 662 * x ** 23 / 10438212015
            + 4 * x ** 27 / 3341878155 + x ** 31 / 109876902975)

def picard(xMax, step, picardFunc):
    res = np.array([])

    for x in np.arange(0, xMax, step):
        res = np.append(res, picardFunc(x))

    return res


def function(x, u):
    return x ** 2 + u ** 2


def euler(xMax, step):
    res = np.array([])
    u = 0

    for x in np.arange(0, xMax, step):
        res = np.append(res, u)
        u += step * function(x, u)

    return res


def rungeKutta2(xMax, step, alpha):
    res = np.array([])
    u = 0
    k1 = 1 - alpha
    k2 = step / 2 / alpha

    for x in np.arange(0, xMax, step):
        res = np.append(res, u)
        curFunc = function(x, u)
        u += step * (k1 * curFunc + alpha *
                function(x + k2, u + k2 * curFunc))

    return res


def main():
    table = PrettyTable()

    table.add_column("x", np.arange(0, XMAX + 0.01, TABLESTEP))
    table.add_column("Picard 1st", picard(XMAX + 0.01, STEP, picard1st)[::NUM])
    table.add_column("Picard 2nd", picard(XMAX + 0.01, STEP, picard2nd)[::NUM])
    table.add_column("Picard 3d",  picard(XMAX + 0.01, STEP, picard3d)[::NUM])
    table.add_column("Picard 4th", picard(XMAX + 0.01, STEP, picard4th)[::NUM])
    table.add_column("Euler", euler(XMAX + 0.01, STEP)[::NUM])
    table.add_column("Runge", rungeKutta2(XMAX + 0.01, STEP, 0.5)[::NUM])

    table.float_format = '9.5'
    print(table)


if __name__ == '__main__':
    main()
