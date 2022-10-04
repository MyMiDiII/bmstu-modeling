from typing import Callable

import distributions as dst
import numpy as np

import matplotlib.pyplot as plt

def GetUniformTableFunc(func: Callable[[float, float, float], float],
                        a: float, b: float, intervalsNum: int) -> float:
    xLeft = 2 * a - b
    xRight = 2 * b - a
    step = (xRight - xLeft) / intervalsNum

    xColumn = list(np.arange(xLeft, xRight + step / 2, step))
    print(xColumn)
    yColumn = []

    for x in xColumn:
        yColumn.append(func(x, a, b))

    return xColumn, yColumn


def GetNormalTableFunc(func: Callable[[float, float, float], float],
                       m: float, sigma: float, intervalsNum: int) -> float:
    xLeft = m - 4 * sigma
    xRight = m + 4 * sigma
    step = (xRight - xLeft) / intervalsNum

    xColumn = list(np.arange(xLeft, xRight + step / 2, step))
    print(xColumn)
    yColumn = []

    for x in xColumn:
        yColumn.append(func(x, m, sigma))

    return xColumn, yColumn


if __name__ == "__main__":
    print("Равномерное")
    a = float(input("a = "))
    b = float(input("b = "))
    print("Нормальное")
    m = float(input("m = "))
    sigma = float(input("sigma = "))

    x, y = GetUniformTableFunc(dst.UniformDensityFunc, a, b, 1000)
    plt.plot(x, y)
    plt.show()

    x, y = GetUniformTableFunc(dst.UniformDistributionFunc, a, b, 1000)
    plt.plot(x, y)
    plt.show()

    x, y = GetNormalTableFunc(dst.NormalDensityFunc, m, sigma, 1000)
    plt.plot(x, y)
    plt.show()

    x, y = GetNormalTableFunc(dst.NormalDistributionFunc, m, sigma, 1000)
    plt.plot(x, y)
    plt.show()
