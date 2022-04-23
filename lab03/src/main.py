from numpy import exp
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import numpy as np


c = 3e10
R = 0.35
Tw = 2000
T0 = 10000
k0 = 8e-4
p = 4
m = 0.786

zInit = 0
zMax = 1
zStep = 1e-2
EPS = 1e-6


def T(z):
    return (Tw - T0) * z ** p + T0


def k(z):
    return k0 * (T(z) / 300) ** 2


def Up(z):
    return 3.084e-4 / (exp(4.799e4 / T(z)) - 1)


# def derF(z, F, U):
#     commonPart = R * c * k(z) * (Up(z) - U)
#     return -F / z + commonPart if abs(z) > EPS else commonPart / 2


def divF(z, u):
    return c * k(z) * (Up(z) - u)


def Kn(z):
    return c / (3 * R * k(z))


def kappaHalf(z):
    return (Kn(z + zStep / 2) + Kn(z - zStep / 2)) / 2


def Fn(z):
    return c * k(z) * Up(z)


def Pn(z):
    return c * k(z)


def Vn(z):
     return ((z + zStep / 2)**2 - (z - zStep / 2)**2) / 2


def A(z):
    return (z - zStep / 2) * (kappaHalf(z - zStep / 2))

def C(z):
    return ((z + zStep / 2) * kappaHalf(z + zStep / 2))

def B(z):
    return A(z) + C(z) + Pn(z) * z * zStep ** 2 * R

def D(z):
    return Fn(z) * z * zStep ** 2 * R


def leftCond(z0, F0, h):
    M0 = (kappaHalf(z0 + h / 2) * (z0 + h / 2)
            + c * R * h * h / 16 * k(z0 + h / 2) * (z0 + h / 2))
    K0 = (-kappaHalf(z0 + h / 2) * (z0 + h / 2) 
            + c * R * h * h / 16 * k(z0 + h / 2) * (z0 + h / 2))
    P0 = c * R * h * h / 8 * k(z0 + h / 2) * Up(z0 + h / 2) * (z0 + h / 2)

    return K0, M0, P0


def rightCond(z, h):
    KN = (kappaHalf(z - h / 2) * (z - h / 2) + m * c * z * h / 2
            + c * R * h * h / 8 * k(z - h / 2) * (z - h / 2)
            + R * c * h * h * k(z) / 4)
    MN = (-kappaHalf(z - h / 2) * (z - h / 2)
            + c * R * h * h / 8 * k(z - h / 2) * (z - h / 2))
    PN = (c * R * h * h / 4 * (k(z - h / 2) * Up(z - h / 2) * (z - h / 2)
            + k(z) * Up(z)))

    return KN, MN, PN


def ThomasAlg():
    # Прямой ход
    h = zStep
    K0, M0, P0 = leftCond(0, 0, zStep)
    KN, MN, PN = rightCond(1, zStep)

    eps = [0, -K0 / M0]
    eta = [0, P0 / M0]
    x = h
    n = 1

    while x < zMax + h / 2:
        eps.append(C(x) / (B(x) - A(x) * eps[n]))
        eta.append((A(x) * eta[n] + D(x)) / (B(x) - A(x) * eps[n]))

        n += 1
        x += h

    # Обратный ход
    u = [0] * (n)

    u[n-1] = (PN - MN * eta[n]) / (KN + MN * eps[n])

    for i in range(n - 2, -1, -1):
        u[i] = eps[i + 1] * u[i + 1] + eta[i + 1]

    return u


def centerDer(y, h):
    res = []
    res.append((-3 * y[0] + 4 * y[1] - y[2]) / 2 / h)

    for i in range(1, len(y) - 1):
        r = (y[i + 1] - y[i - 1]) / 2 / h
        res.append(r)

    res.append((3 * y[-1] - 4 * y[-2] + y[-3]) / 2 / h)

    return res


def getFDer(u, z):
    f = [0]
    uDer = centerDer(u, zStep)

    for i in range(1, len(z)):
        r = -c / 3 / R / k(z[i]) * uDer[i]
        f.append(r)

    return f


def getFInt(z, un, un1, f):
    if abs(z - 1) < 1e-4:
        return m * c * un / 2

    return kappaHalf(z - zStep / 2) * (un - un1) / zStep


class Table(PrettyTable):
    def add_columns(self, colDict : dict):
        for key, value in colDict.items():
            self.add_column(key, value[0], align="r")
            self.custom_format[key] = value[1]


class Graphics:
    def __init__(self, graphics=[]):
        self.graphics = graphics
        self.num = len(graphics)


    def addGraphic(self, xVals, yVals, labels, title):
        self.graphics.append({
                        "x" : xVals,
                        "y" : yVals,
                        "labels" : labels,
                        "title" : title
                        })
        self.num += 1


    def show(self):
        for i, graph in enumerate(self.graphics):
            plt.subplot(2, self.num // 2 + self.num % 2, i + 1)

            for j, y in enumerate(graph["y"]):
                plt.plot(graph["x"], y, label=graph["labels"][j])

            plt.legend()
            plt.title(graph["title"])
            plt.grid()

        plt.subplots_adjust(wspace=0.3, hspace=0.3)
        plt.show()


if __name__ == "__main__":
    name = ['U(z)', 'F(z)']
    uRes = ThomasAlg()
    zRes = [i for i in np.arange(0, 1 + zStep, zStep)]

    fRes = [0] * len(zRes)
    upRes = [0] * len(zRes)
    divF_ = [0] * len(zRes)

    FDer = getFDer(uRes, zRes)

    for i in range(0, len(zRes) - 1):
        upRes[i] = Up(zRes[i])
        divF_[i] = divF(zRes[i], uRes[i])

    for i in range(1, len(zRes)):
        fRes[i] = getFInt(zRes[i], uRes[i - 1], uRes[i], fRes[i - 1])

    table = Table()
    columns = {
            "z" : (zRes, lambda f, v: f"{v:.2f}"),
            "F(z)" : (fRes, lambda f, v: f"{v:.3f}"),
            "Fder(z)" : (FDer, lambda f, v: f"{v:.3f}"),
            "U(z)" : (uRes, lambda f, v: f"{v:.4e}"),
            "divF(z)" : (divF_, lambda f, v: f"{v:.3f}")
    }
    table.add_columns(columns)
    print(table)

    graphics = Graphics()
    graphics.addGraphic(zRes, [uRes, upRes], ["U", "Up"], "U(z), Up(z)")
    graphics.addGraphic(zRes, [fRes],  [""], "F(z)")
    graphics.addGraphic(zRes, [divF_], [""], "divF")
    graphics.addGraphic(zRes, [FDer], [""], "Fder")
    graphics.show()

