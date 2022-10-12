def NormalDensityFunc(x: float, m: float, sigma: float) -> float:
    return (1 / sqrt(2 * pi) / sigma
                * exp(- ((x - m) / sigma) ** 2 / 2)
                    if sigma > 0 else -1)
