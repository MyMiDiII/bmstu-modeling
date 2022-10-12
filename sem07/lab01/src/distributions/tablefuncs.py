from typing import Callable, Tuple

import distributions.distributions as dst
import numpy as np

import matplotlib.pyplot as plt

def GetTableFunc(function: Callable[..., float],
                 arguments: list[float],
                 xLeft: float,
                 xRight: float,
                 stepsNum: int) -> Tuple[list[float], list[float]]:
    step = (xRight - xLeft) / stepsNum

    xColumn = list(np.arange(xLeft, xRight + step / 2, step))
    yColumn = []

    for x in xColumn:
        yColumn.append(function(x, *arguments))

    return xColumn, yColumn


def GetUniformTableFunc(
        func:      Callable[[float, float, float], float],
        arguments: Tuple[float, float],
        interval:  Tuple[float, float],
        stepsNum:  int) -> Tuple[list[float], list[float]]:

    a, b = arguments

    xLeft, xRight = (2 * a - b, 2 * b - a) if interval is None else interval

    return GetTableFunc(func, [a, b], xLeft, xRight, stepsNum)


def GetNormalTableFunc(
        func:      Callable[[float, float, float], float],
        arguments: Tuple[float, float],
        interval:  Tuple[float, float],
        stepsNum:  int) -> Tuple[list[float], list[float]]:

    m, sigma = arguments

    xLeft, xRight = ((m - 4 * sigma, m + 4 * sigma)
                        if interval is None else interval)

    return GetTableFunc(func, [m, sigma], xLeft, xRight, stepsNum)


def GetUniformDensityTableFunc(
        a: float,
        b: float,
        stepsNum: int,
        interval: Tuple[float, float] = None) -> Tuple[list[float], list[float]]:
    return GetUniformTableFunc(dst.UniformDensityFunc, [a, b], interval, stepsNum)


def GetUniformDistributionTableFunc(
        a: float,
        b: float,
        stepsNum: int,
        interval: Tuple[float, float] = None) -> Tuple[list[float], list[float]]:
    return GetUniformTableFunc(dst.UniformDistributionFunc, [a, b],
                               interval, stepsNum)


def GetNormalDensityTableFunc(
        m:     float,
        sigma: float,
        stepsNum: int,
        interval: Tuple[float, float] = None) -> Tuple[list[float], list[float]]:
    return GetNormalTableFunc(dst.NormalDensityFunc, [m, sigma], interval, stepsNum)


def GetNormalDistributionTableFunc(
        m:     float,
        sigma: float,
        stepsNum: int,
        interval: Tuple[float, float] = None) -> Tuple[list[float], list[float]]:
    return GetNormalTableFunc(dst.NormalDistributionFunc, [m, sigma],
                              interval, stepsNum)


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
