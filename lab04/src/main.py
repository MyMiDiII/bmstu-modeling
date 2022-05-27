from numpy import e
import matplotlib.pyplot as plt
import numpy as np
from math import fabs, sin, pi
from mpl_toolkits.mplot3d import Axes3D
from data import data

ti_max = 500


class Function:
    def __init__(self):
        self.k0 = data['k0']
        self.a1 = data['a1']
        self.b1 = data['b1']
        self.c1 = data['c1']
        self.m1 = data['m1']
        self.a2 = data['a2']
        self.b2 = data['b2']
        self.c2 = data['c2']
        self.m2 = data['m2']
        self.l = data['l']
        self.T0 = data['T0']
        self.R = data['R']
        self.tau = data['tau']

        self.x0 = data['x0']

        self.alpha0 = data['alpha0']
        self.alphaN = data['alphaN']

        self.Fmax = data['Fmax']
        self.tmax = data['tmax']

        self.h = data['h']
        self.EPS = 1e-4


    def alpha(self, x):
        d = (self.alphaN * self.l) / (self.alphaN - self.alpha0)
        c = -self.alpha0 * d
        return c / (x - d)


    def p(self, x):
        return 2 * self.alpha(x) / self.R


    def k(self, T):
        return self.k0 * ((T / 300)**2)


    def lamda(self, T):
        return self.a1 * (self.b1 + self.c1 * T**self.m1)

    def c(self, T):
        return self.a2 + self.b2 * T ** self.m2 - (self.c2 / T ** 2)

    def f2(self, x):
        return 2 * self.T0 * self.alpha(x) / self.R


    def F0(self, t):
        period = data['period']
        tu = data['tu']
        #print(t)
        #return 10
        print(t)
        print(100 * fabs(sin(100 * pi * t)))
        return 100 * fabs(sin(100 * pi * t))
        #if (t % period <= tu):
            #return self.Fmax / self.tmax * t * e**(-(t / self.tmax - 1))
        #return self.Fmax / self.tmax * t * e**(-(t / self.tmax - 1))
        # return 10


class Lab4(Function):
    def func_plus_half(self, x, h, func):
        return (func(x) + func(x + h)) / 2

    def func_minus_half(self, x, h, func):
        return (func(x) + func(x - h)) / 2


    def A(self, T, n):
        return self.tau * (self.lamda(T[n]) + self.lamda(T[n - 1])) / self.h / 2

    def D(self, T, n):
        return self.tau * (self.lamda(T[n]) + self.lamda(T[n + 1])) / self.h / 2

    def B(self, x, T, n):
        return self.A(T, n) + self.D(T, n) + self.c(T[n]) * self.h + self.p(x) * self.tau * self.h

    def G(self, x, T, n, ti):
        g1 = self.c(T[n]) * self.h * T[n]
        g2 = self.h * self.tau * self.k(T[n]) * self.F0(ti) * e**(-self.k(T[n]) * x)
        g3 = self.f2(x) * self.h * self.tau
        return g1 + g2 + g3

    def left_bc(self, T_prev, time):
        h = self.h
        k1 = h * (self.c(T_prev[0]) + self.c(T_prev[1])) / 16
        k2 = h * self.c(T_prev[0]) / 4
        k3 = self.tau * (self.lamda(T_prev[0]) + self.lamda(T_prev[1])) / h / 2
        k4 = self.tau * h * (self.p(0) + self.p(h)) / 16
        k5 = self.tau * h * self.p(0) / 4
        k6 = self.alpha0 * self.tau
        K0 = k1 + k2 + k3 + k4 + k5 + k6

        m1 = h * (self.c(T_prev[0]) + self.c(T_prev[1])) / 16
        m2 = self.tau * (self.lamda(T_prev[0]) + self.lamda(T_prev[1])) / h / 2
        m3 = self.tau * h * (self.p(0) + self.p(h)) / 16
        M0 = m1 - m2 + m3

        p1 = h * (self.c(T_prev[0]) + self.c(T_prev[1])) * (T_prev[0] + T_prev[1]) / 16
        p2 = h * self.c(T_prev[0]) * T_prev[0] / 4
        p3 = self.alpha0 * self.T0 * self.tau
        p4 = 2 * self.T0 / 2 / self.R * (3 * self.alpha0 + self.alpha(h)) * h * self.tau / 4
        p5 = h * self.tau * self.F0(time) * self.k(T_prev[0]) * e**(-self.k(T_prev[0]) * 0) / 4

        p6 = h * self.tau * self.F0(time) * (self.k(T_prev[0]) + self.k(T_prev[1])) / 2 * e**(-(self.k(T_prev[0]) + self.k(T_prev[1])) / 2 * (0 + h / 2)) / 4

        P0 = p1 + p2 + p3 + p4 + p5 + p6

        return K0, M0, P0

    def right_bc(self, T_prev, time):
        h = self.h
        k1 = h * self.c(T_prev[-1]) / 4
        k2 = h * (self.c(T_prev[-1]) + self.c(T_prev[-2])) / 16
        k3 = self.tau * (self.lamda(T_prev[-1]) + self.lamda(T_prev[-2])) / h / 2
        k4 = self.tau * h * self.p(self.l) / 4
        k5 = self.tau * h * (self.p(self.l) + self.p(self.l - h)) / 16
        k6 = - self.alphaN * self.tau
        KN = k1 + k2 + k3 + k4 + k5 + k6

        m1 = h * (self.c(T_prev[-1]) + self.c(T_prev[-2])) / 16
        m2 = self.tau * (self.lamda(T_prev[-1]) + self.lamda(T_prev[-2])) / h / 2
        m3 = self.tau * h * (self.p(self.l) + self.p(self.l - h)) / 16
        MN = m1 - m2 + m3

        p1 = h * (self.c(T_prev[-1]) + self.c(T_prev[-2])) / 2 * (T_prev[-1] +
                T_prev[-2]) / 8
        p2 = - self.tau * self.alphaN * self.T0
        p3 = self.tau * h * (3 * self.f2(self.l) + self.f2(self.l - h)) / 8
        p4 = h * self.c(T_prev[-1]) * T_prev[-1] / 4
        p5 = (h * self.tau * self.F0(time) * self.k(T_prev[-1])
                * e ** (-self.k(T_prev[-1]) * self.l) / 4)
        p6 = (h * self.tau * self.F0(time) * (self.k(T_prev[-1]) +
                self.k(T_prev[-2])) / 2 * e**(-(self.k(T_prev[-1]) +
                    self.k(T_prev[-2])) / 2 * (self.l - h / 2)) / 4)
        PN = p1 + p2 + p3 + p4 + p5 + p6

        return KN, MN, PN


    def run(self, T_prev, K0, M0, P0, KN, MN, PN, ti):
        h = self.h
        eps = [0, -M0 / K0]
        eta = [0, P0 / K0]
        x = h
        n = 1
        while (x + h < self.l):
            eps.append(self.D(T_prev, n) / (self.B(x, T_prev, n) - self.A(T_prev, n) * eps[n]))
            eta.append((self.G(x, T_prev, n, ti) + self.A(T_prev, n) * eta[n]) / (self.B(x, T_prev, n) - self.A(T_prev, n) * eps[n]))
            n += 1
            x += h

        y = [0] * (n + 1)
        y[n] = (PN - MN * eta[n]) / (KN + MN * eps[n])

        for i in range(n - 1, -1, -1):
            y[i] = eps[i + 1] * y[i + 1] + eta[i + 1]

        return y


class Res(Lab4):
    def res(self):
        h = self.h
        step1 = int(self.l / h)
        T = [self.T0] * (step1 + 1)

        ti = 0
        res = []
        res.append(T)

        ff = 0
        while True:
            prev = T
            ti += self.tau
            while True:
                K0, M0, P0 = self.left_bc(prev, ti)
                KN, MN, PN = self.right_bc(prev, ti)

                T_new = self.run(prev, K0, M0, P0, KN, MN, PN, ti)

                max = (T[0] - T_new[0]) / T_new[0]
                max = abs(max)
                for step2, j in zip(T, T_new):
                    d = (step2 - j) / j
                    d = abs(d)
                    if d > max:
                        max = d
                if max < 1:
                    break

                prev = T_new
            res.append(T_new)
            ff += 1

            check_eps = 0
            for i, j in zip(T, T_new):
                tttt = fabs((i - j) / j)
                if fabs((i - j) / j) > self.EPS:
                    check_eps = 1
            if check_eps == 0:
                break
            T = T_new

        return res, ti


    def draw(self):
        h = self.h
        res, ti = self.res()
        x = [i for i in np.arange(0, self.l, h)]
        te = [i for i in np.arange(0, ti, self.tau)]

# 3д график
        xgrid, ygrid = np.meshgrid(x, te)
        zgrid = [i[:-1] for i in res]
        zgrid.pop()
        xgrid = np.array(xgrid)
        ygrid = np.array(ygrid)
        zgrid = np.array(zgrid)

        fig = plt.figure(figsize=(7, 4))
        ax_3d = Axes3D(fig)
        ax_3d.plot_surface(ygrid, xgrid, zgrid, cmap='GnBu')
        ax_3d.set_ylabel("x, cm")
        ax_3d.set_xlabel("t, c")
        ax_3d.set_zlabel("T, K")
        plt.show()

# группа 2д графиков
        plt.subplot(2, 1, 1)
        step1 = 0
        for_graph = ti_max / 10
        for i in res:
            if (step1 % for_graph == 0):
                namestr = "t = " + str(step1)
                plt.plot(x, i[:-1], label=namestr)
            step1 += 1

        plt.plot(x, res[-1][:-1])
        plt.xlabel("x, cm")
        plt.ylabel("T, K")
        plt.legend()
        plt.grid()

        plt.subplot(2, 1, 2)
        step2 = 0
        iter = 0
        l = int(self.l / self.h)
        while iter < 10:
            point = [j[int(step2 / h)] for j in res]
            namestr = "x = " + str(round(step2, 1))
            plt.plot(te, point[:-1], label=namestr)
            step2 += 0.1 * 10
            iter += 1

        plt.xlabel("t, sec")
        plt.ylabel("T, K")
        plt.grid()

        plt.show()


    def step_t(self):
        h = self.h
        deltah = [1, 0.1, 0.01, 0.001]
        result = []
        for hi in deltah:
            self.tau = hi
            res, ti = self.res()

            n = 0
            for temp in res:
                if (fabs(n - 1) < self.EPS):
                    print()
                    print(self.tau)
                    print()
                    result.append(temp[:-1])
                n += self.tau
        print('    1    |   0.1   |   0.01  |  0.001  |')
        for i in range(len(result[0])):
            for j in range(len(result)):
                print(' %3.3f |' % result[j][i], end='')
            print()

    def step_t2(self):
        deltah = [1, 0.1, 0.01, 0.001]
        result = []
        for hi in deltah:
            self.h = hi
            h = self.h
            res, ti = self.res()
            print(h)
            i = 0
            xfix = [temp[int(i / h)] for temp in res]
            result.append(xfix)

        print('    1    |   0.1   |   0.01  |  0.001  |')
        for i in range(len(result[0])):
            for j in range(len(result)):
                print(' %3.3f |' % result[j][i], end='')
            print()


    def a_b(self):
        h = self.h
        t = self.tau
        arraya2 = [2.049, 5, 10, 15, 50]
        arrayb2 = [0.000564, 0.001, 0.01, 0.1, 5]
        result = []
        resulti = []
        for ai, bi in zip(arraya2, arrayb2):
            self.a2 = ai
            self.b2 = bi
            res, ti = self.res()

            te = []
            i = 0
            while (i < ti):
                te.append(i)
                i += t

            i = 0
            xfix = [temp[int(i / h)] for temp in res]
            print(xfix[:-1])
            result.append(xfix[:-1])
            resulti.append(te)

        for res, teres in zip(result, resulti):
            plt.plot(teres, res)

        plt.xlabel("Время, c")
        plt.ylabel("Температура, K")
        plt.show()


    def chast(self): # надо поменять в F0: return 0 поставить
        res, ti = self.res()

        te = []
        i = 0
        while (i < ti):
            te.append(i)
            i += self.tau
        i = 0
        xfix = [temp[int(i / self.h)] for temp in res]
        plt.plot(te, xfix[1:])
        plt.xlabel("Время, c")
        plt.ylabel("Температура, K")
        plt.show()

def main():
    resh = Res()
    print(resh.draw())
    resh.chast()

if __name__ == "__main__":
    main()
