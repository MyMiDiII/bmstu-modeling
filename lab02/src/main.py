from math import exp

import numpy as np
from prettytable import PrettyTable

EPS = 1e-4
MAX_ITER_NUMS = 100

class RadiativeTransfer:

    def __init__(self, c=3e10, R=0.35, Tw=2000,
                       T0=10000, k0=8e-3, p=4, m=0.786):
        self.c  = c # см/с
        self.R  = R # см
        self.Tw = Tw # К
        self.T0 = T0 # К
        self.k0 = k0 # 1/см
        self.p  = p
        self.m  = m


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


    def RungeKutta4(self, zStep, zInit, zMax, uInit, fInit):
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


    def psi(self, U, F):
        return F - self.m * self.c * U / 2


    def psiEnd(self, xi):
        _, u, f = self.RungeKutta4(1e-2, 0, 1, xi * self.Up(0), 0)
        return self.psi(u[-1], f[-1])


    def getXiInterval(self):
        xiCur = 1e-2
        step = 1e-2
        xiMax = 1

        xiFrom, psiFrom = xiCur, self.psiEnd(xiCur)
        xiTo, psiTo = xiCur + step, self.psiEnd(xiCur + step)

        while xiTo < xiMax - step / 2 and psiFrom * psiTo > 0:
            xiFrom, psiFrom = xiTo, psiTo
            xiTo, psiTo = xiFrom + step, self.psiEnd(xiFrom + step)

        return xiFrom, xiTo


    def getXi(self):
        xiFrom, xiTo = self.getXiInterval()
        xiCur = xiFrom - xiTo
        iterNum = 0

        while abs((xiFrom - xiTo) / xiCur) > EPS and iterNum < MAX_ITER_NUMS:
            xiCur = (xiFrom + xiTo) / 2

            if self.psiEnd(xiFrom) * self.psiEnd(xiCur) < 0:
                xiTo = xiCur
            else:
                xiFrom = xiCur

            iterNum += 1

        return xiCur


    def getU0(self):
        return self.getXi() * self.Up(0)


    def solve(self):
        step = 1e-2
        zInit = 0
        zMax = 1
        f0 = 0
        u0 = self.getU0()

        return system.RungeKutta4(step, zInit, zMax, u0, f0)


class Table(PrettyTable):
    def add_columns(self, colDict : dict):
        for key, value in colDict.items():
            self.add_column(key, value[0], align="r")
            self.custom_format[key] = value[1]


if __name__ == '__main__':
    system = RadiativeTransfer()
    z, u, f = system.solve()

    table = Table()
    columns = {
            "z" : (z, lambda f, v: f"{v:.2f}"),
            "u(z)" : (u, lambda f, v: f"{v:.4e}"),
            "f(z)" : (f, lambda f, v: f"{v:.3f}")
    }
    table.add_columns(columns)
    print(table)

