def NormalDistributionFunc(x: float,
                           m: float, sigma: float) -> float:
    return ((1 + erf((x - m) / sigma / sqrt(2))) / 2
            if sigma > 0 else -1)
