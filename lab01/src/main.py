from prettytable import PrettyTable
import numpy as np


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


def main():
    table = PrettyTable()

    table.add_column("x", np.arange(0, 2.01, 0.05))
    table.add_column("Picard 1st", picard(2.01, 1e-4, picard1st)[::500])
    table.add_column("Picard 2nd", picard(2.01, 1e-4, picard2nd)[::500])
    table.add_column("Picard 3d",  picard(2.01, 1e-4, picard3d)[::500])
    table.add_column("Picard 4th", picard(2.01, 1e-4, picard4th)[::500])

    table.float_format = '.6'
    print(table)


if __name__ == '__main__':
    main()
