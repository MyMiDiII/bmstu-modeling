from math import exp

import numpy as np
from prettytable import PrettyTable

EPS = 1e-4

class RadiativeTransfer:

    def __init__(self, c, R, Tw, T0, k0, p):
        self.c  = c # см/с
        self.R  = R # см
        self.Tw = Tw # К
        self.T0 = T0 # К
        self.k0 = k0 # 1/см
        self.p  = p

    def T(self, z):
        return (self.Tw - self.T0) * z ** self.p + self.T0

    def k(self, z):
        return self.k0 * (self.T(z) / 300) ** 2

    def derU(self, z, F):
        return - 3 * self.R * self.k(z) / self.c * F

    def Up(self, z):
        return 3.084e-4 / (exp(4.799e4 / self.T(z)) - 1)

    def derF(self, z, F, U):
        commonPart = self.R * self.c * self.k(z) * (self.Up(z) - U)
        return -F / z + commonPart if abs(z) > EPS else commonPart / 2


    def RungeKutta4(self, zStep, zInit, zMax, fInit, uInit):
        halfStep = zStep / 2

        zRes = np.arange(zInit, zMax + halfStep, zStep)
        uRes = np.zeros(len(zRes))
        fRes = np.zeros(len(zRes))

        uCur = uInit
        fCur = fInit

        for i, z in enumerate(zRes):
            uRes[i] = uCur
            fRes[i] = fCur

            k1 = zStep * self.derU(z, fCur)
            l1 = zStep * self.derF(z, fCur, uCur)

            halfL1 = l1 / 2
            k2 = zStep * self.derU(z + halfStep, fCur + halfL1)
            l2 = zStep * self.derF(z + halfStep, fCur + halfL1, uCur + k1 / 2)

            halfL2 = l2 / 2
            k3 = zStep * self.derU(z + halfStep, fCur + halfL2)
            l3 = zStep * self.derF(z + halfStep, fCur + halfL2, uCur + k2 / 2)

            k4 = zStep * self.derU(z + zStep, fCur + l3)
            l4 = zStep * self.derF(z + zStep, fCur + l3, uCur + k3)

            uCur += (k1 + 2 * k2 + 2 * k3 + k4) / 6
            fCur += (l1 + 2 * l2 + 2 * l3 + l4) / 6

        return zRes, uRes, fRes


class Table(PrettyTable):
    def add_columns(self, colDict : dict):
        for key, value in colDict.items():
            self.add_column(key, value[0], align="r")
            self.custom_format[key] = value[1]


if __name__ == '__main__':
    system = RadiativeTransfer(3e10, 0.35, 2000, 10000, 8e-4, 4)
    print(0.86*system.Up(0))
    z, u, f = system.RungeKutta4(1e-2, 0, 1, 0, 0.86 * system.Up(0))

    table = Table()
    columns = {
            "z" : (z, lambda f, v: f"{v:.2f}"),
            "u(z)" : (u, lambda f, v: f"{v:.3e}"),
            "f(z)" : (f, lambda f, v: f"{v:.3f}")
    }
    table.add_columns(columns)
    print(table)

