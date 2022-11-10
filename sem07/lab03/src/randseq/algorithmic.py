from abc import ABC, abstractmethod

import matplotlib.pyplot as plt

class Generator:

    def __init__(self, normGen):
        self.normGen = normGen


    def GenerateNumber(self, lower, upper):
        return round(self.normGen.GetNumber01() * (upper - lower) + lower)


class QuadaticGenerator(Generator):

    def __init__(self):
        super().__init__(QuadaticRandom())


class CoveyouGenerator(Generator):

    def __init__(self):
        super().__init__(CoveyouRandom())


class LinearGenerator(Generator):

    def __init__(self):
        super().__init__(LinearRandom())


class NormalizedRandom(ABC):

    @abstractmethod
    def GetNumber01(self):
        pass


class QuadaticRandom(NormalizedRandom):

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


class CoveyouRandom(NormalizedRandom):

    def __init__(self):
        self.current = 2135
        self.m = 8192


    def GetNumber01(self):
        self.current = self.current * (self.current + 1) % self.m
        return self.current / self.m


class LinearRandom(NormalizedRandom):

    def __init__(self):
        self.current = 10
        self.m = 312500
        self.a = 36261
        self.c = 66037


    def GetNumber01(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current / self.m


def main():
    numbers = 5000
    lower = 0
    upper = 100

    generators = [
         QuadaticGenerator(),
         CoveyouGenerator(),
         LinearGenerator(),
    ]

    ys = [[], [], []]

    for _ in range(numbers):
        for i, generator in enumerate(generators):
            num = generator.GenerateNumber(lower, upper)
            print(num)
            ys[i].append(num)

    x = [i for i in range(numbers)]

    graphConf = [
            {"label" : "квадратичный", "color" : "b"},
            {"label" : "Ковэю", "color" : "g"},
            {"label" : "линейный", "color" : "orange"},
    ]

    for i, y in enumerate(ys):
        plt.figure()
        plt.plot(x, y, label=graphConf[i]["label"], color=graphConf[i]["color"])
        plt.legend()

    for el in ys:
        x = el[:-1]
        y = el[1:]

        plt.figure()
        plt.plot(x, y, "o")

    plt.show()


if __name__ == "__main__":
    main()

