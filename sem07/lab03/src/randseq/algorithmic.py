import random

import matplotlib.pyplot as plt

class QuadaticRandom:

    def __init__(self):
        self.current = 4001
        self.A = 6
        self.B = 7
        self.C = 3
        self.m = 4096


    def GetNumber01(self):
        self.current = (self.A * self.current * self.current
                        + self.B * self.current
                        + self.C) % self.m
        return self.current / self.m


class CoveyouRandom:

    def __init__(self):
        self.current = 2135
        self.m = 512


    def GetNumber01(self):
        self.current = self.current * (self.current + 1) % self.m
        return self.current / self.m


class LinearRandom:

    def __init__(self):
        self.current = 10
        self.m = 312500
        self.a = 36261
        self.c = 66037

    def GetNumber01(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current / self.m


def main():
    genQuad = QuadaticRandom()
    genCove = CoveyouRandom()
    genLin = LinearRandom()

    yQuad = []
    yCove = []
    yLin = []

    for i in range(1000):
        num = genQuad.GetNumber01()
        yQuad.append(num * 100)
        print(round(num * 100))

        num = genCove.GetNumber01()
        yCove.append(num * 100)
        print(round(num * 100))

        num = genLin.GetNumber01()
        yLin.append(num * 100)
        print(round(num * 100))

    x = [i for i in range(1000)]
    plt.figure()
    plt.plot(x, yQuad, label="квадратичный")
    plt.legend()

    plt.figure()
    plt.plot(x, yCove, "g", label="Ковэю")
    plt.legend()

    plt.figure()
    plt.plot(x, yLin, color="orange", label="линейный")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

