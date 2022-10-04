from math import sqrt, pi, exp, erf

def UniformDensityFunc(x: float, a: float, b: float) -> float:
    return 0 if x < a or x > b else 1 / (b - a)


def UniformDistributionFunc(x: float, a: float, b: float) -> float:
    if x < a:
        return 0

    if x > b:
        return 1

    return (x - a) / (b - a)


def NormalDensityFunc(x: float, m: float, sigma: float) -> float:
    return (1 / sqrt(2 * pi) / sigma * exp(- ((x - m) / sigma) ** 2 / 2)
            if sigma > 0 else -1)


def NormalDistributionFunc(x: float, m: float, sigma: float) -> float:
    return (1 + erf((x - m) / sigma / sqrt(2))
            if sigma > 0 else -1)
