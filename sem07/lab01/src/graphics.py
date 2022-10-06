from typing import Callable, Tuple

import distributions as dst
import numpy as np

import matplotlib.pyplot as plt

def GetUniformTableFunc(func: Callable[[float, float, float], float],
                        a: float,
                        b: float,
                        intervalsNum: int) -> Tuple[list[float], list[float]]:
    xLeft = 2 * a - b
    xRight = 2 * b - a
    step = (xRight - xLeft) / intervalsNum

    xColumn = list(np.arange(xLeft, xRight + step / 2, step))
    yColumn = []

    for x in xColumn:
        yColumn.append(func(x, a, b))

    return xColumn, yColumn


def GetNormalTableFunc(func: Callable[[float, float, float], float],
                       m: float,
                       sigma: float,
                       intervalsNum: int) -> Tuple[list[float], list[float]]:
    xLeft = m - 4 * sigma
    xRight = m + 4 * sigma
    step = (xRight - xLeft) / intervalsNum

    xColumn = list(np.arange(xLeft, xRight + step / 2, step))
    yColumn = []

    for x in xColumn:
        yColumn.append(func(x, m, sigma))

    return xColumn, yColumn


def GetUniformDensityTableFunc(a: float, b: float,
                       intervalsNum: int) -> Tuple[list[float], list[float]]:
    return GetUniformTableFunc(dst.UniformDensityFunc, a, b, intervalsNum)


def GetNormalDensityTableFunc(m: float, sigma: float,
                       intervalsNum: int) -> Tuple[list[float], list[float]]:
    return GetNormalTableFunc(dst.NormalDensityFunc, m, sigma, intervalsNum)


def GetUniformDistributionTableFunc(a: float, b: float,
                       intervalsNum: int) -> Tuple[list[float], list[float]]:
    return GetUniformTableFunc(dst.UniformDistributionFunc, a, b, intervalsNum)


def GetNormalDistributionTableFunc(m: float, sigma: float,
                       intervalsNum: int) -> Tuple[list[float], list[float]]:
    return GetNormalTableFunc(dst.NormalDistributionFunc, m, sigma, intervalsNum)


def graphics():
    print("Равномерное")
    a = float(input("a = "))
    b = float(input("b = "))
    print("Нормальное")
    m = float(input("m = "))
    sigma = float(input("sigma = "))

    x, y = GetUniformDensityTableFunc(a, b, 1000)
    plt.plot(x, y)
    plt.show()

    x, y = GetUniformDistributionTableFunc(a, b, 1000)
    plt.plot(x, y)
    plt.show()

    x, y = GetNormalDensityTableFunc(m, sigma, 1000)
    plt.plot(x, y)
    plt.show()

    x, y = GetNormalDistributionTableFunc(m, sigma, 1000)
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    graphics()
