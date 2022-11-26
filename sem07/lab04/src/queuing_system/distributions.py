import numpy.random as nprand

class Uniform:

    def __init__(self, a, b):
        self.a = min(a, b)
        self.b = max(a, b)


    def generate(self):
        return nprand.uniform(self.a, self.b)


class Normal:

    def __init__(self, m, sigma):
        self.m = m
        self.sigma = sigma


    def generate(self):
        return nprand.normal(self.m, self.sigma)


if __name__ == "__main__":
    uniform = Uniform(-10, 10)
    print(uniform.generate())

    normal = Normal(0, 5)
    print(normal.generate())
