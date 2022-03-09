from prettytable import PrettyTable
import numpy as np
import matplotlib.pyplot as plt

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
    xRange = np.arange(0, xMax + step / 2, step)
    res = np.zeros(len(xRange))

    for i, x in enumerate(xRange):
        res[i] = picardFunc(x)

    return res


def function(x, u):
    return x ** 2 + u ** 2


def euler(xMax, step):
    xRange = np.arange(0, xMax + step / 2, step)
    res = np.zeros(len(xRange))
    u = 0

    for i, x in enumerate(xRange):
        res[i] = u
        u += step * function(x, u)

    return res


def rungeKutta2(xMax, step, alpha):
    xRange = np.arange(0, xMax + step / 2, step)
    res = np.zeros(len(xRange))
    u = 0
    k1 = 1 - alpha
    k2 = step / 2 / alpha

    for i, x in enumerate(xRange):
        res[i] = u
        curFunc = function(x, u)
        u += step * (k1 * curFunc + alpha *
                function(x + k2, u + k2 * curFunc))

    return res


def main():
    yPicard1st  = picard(XMAX, STEP, picard1st)
    yPicard2nd  = picard(XMAX, STEP, picard2nd)
    yPicard3d   = picard(XMAX, STEP, picard3d)
    yPicard4th  = picard(XMAX, STEP, picard4th)
    yEuler      = euler(XMAX, STEP)
    yRungeKutta = rungeKutta2(XMAX, STEP, 0.5)

    table = PrettyTable()

    table.add_column("x", np.arange(0, XMAX + 0.01, TABLESTEP))
    table.add_column("Picard 1st", yPicard1st[::NUM])
    table.add_column("Picard 2nd", yPicard2nd[::NUM])
    table.add_column("Picard 3d",  yPicard3d[::NUM])
    table.add_column("Picard 4th", yPicard4th[::NUM])
    table.add_column("Euler", yEuler[::NUM])
    table.add_column("Runge", yRungeKutta[::NUM])

    table.float_format = '9.5'
    print(table)

    fig = plt.figure(figsize=(15, 7))
    ax1 = fig.add_subplot(1, 2, 1)
    
    x = np.arange(-XMAX - STEP / 2, XMAX + STEP / 2, STEP)

    y = picard(-XMAX, -STEP, picard1st)[:-1]
    ax1.plot(x, np.concatenate([np.flip(y), yPicard1st]), label="Пикар 1")

    y = picard(-XMAX, -STEP, picard2nd)[:-1]
    ax1.plot(x, np.concatenate([np.flip(y), yPicard2nd]), label="Пикар 2")

    y = picard(-XMAX, -STEP, picard3d)[:-1]
    ax1.plot(x, np.concatenate([np.flip(y), yPicard3d]), label="Пикар 3")

    y = picard(-XMAX, -STEP, picard4th)[:-1]
    ax1.plot(x, np.concatenate([np.flip(y), yPicard4th]), label="Пикар 4")

    ax2 = fig.add_subplot(2, 2, 2)
    y = euler(-XMAX, -STEP)[:-1]
    ax2.plot(x, np.concatenate([np.flip(y), yEuler]), label="Эйлер")

    ax3 = fig.add_subplot(2, 2, 4)
    y = rungeKutta2(-XMAX, -STEP, 0.5)[:-1]
    ax3.plot(x, np.concatenate([np.flip(y), yRungeKutta]),
                label="Рунге-Кутта")

    for ax in [ax1, ax2, ax3]:
        ax.legend()
        ax.grid()

    plt.show()

if __name__ == '__main__':
    main()
