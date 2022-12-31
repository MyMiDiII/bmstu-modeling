def UniformDensityFunc(x: float, a: float, b: float) -> float:
    return 0 if x < a or x > b else 1 / (b - a)
