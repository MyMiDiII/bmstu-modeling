def UniformDistributionFunc(x: float,
                            a: float, b: float) -> float:
    if x < a:
        return 0

    if x > b:
        return 1

    return (x - a) / (b - a)
