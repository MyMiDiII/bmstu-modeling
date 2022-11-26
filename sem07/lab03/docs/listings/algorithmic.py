class Generator:

    def __init__(self, normGen, lower=0, upper=100):
        self.normGen = normGen
        self.lower = lower
        self.upper = upper

    def GenerateNumber(self):
        return round(self.normGen.GetNumber01()
                     * (self.upper - self.lower) + self.lower)

    def GenerateSequence(self, length):
        return [self.GenerateNumber() for _ in range(length)]


class QuadraticGenerator(Generator):

    def __init__(self, lower, upper):
        super().__init__(QuadraticRandom(), lower, upper)


class QuadraticRandom(NormalizedRandom):

    def __init__(self):
        self.current = 4001
        self.A = 6
        self.B = 7
        self.C = 3
        self.m = 8192

    def GetNumber01(self):
        self.current = (self.A * self.current * self.current
                        + self.B * self.current
                        + self.C) % self.m
        return self.current / self.m
