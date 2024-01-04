import numpy as np

from ElementUniwersalny import ElementUniwersalny
from całki import *
from jakobian import Jakobian


#Macierz współczynników układu równań
class Hmatrix:
    def __init__(self, x, y, e: ElementUniwersalny, k: float):
        self.e = e
        self.j = [Jakobian(x, y, e, i) for i in range(e.n ** 2)]
        self.dNidx = np.zeros([e.n ** 2, 4])
        self.dNidy = np.zeros([e.n ** 2, 4])
        self.h = np.zeros([e.n ** 2, 4, 4])
        self.H = np.zeros([4, 4])
        for i in range(e.n ** 2):
            for j in range(4):
                self.dNidx[i][j] = self.j[i].inv[0][0] * e.dNKsi[i][j] + self.j[i].inv[0][1] * e.dNEta[i][j]
        for i in range(e.n ** 2):
            for j in range(4):
                self.dNidy[i][j] = self.j[i].inv[1][0] * e.dNKsi[i][j] + self.j[i].inv[1][1] * e.dNEta[i][j]
        for i in range(e.n ** 2):
            pom1 = np.array(self.dNidx[i])[np.newaxis]
            pom2 = np.array(self.dNidy[i])[np.newaxis]

            xm = pom1 * pom1.T
            ym = pom2 * pom2.T
            self.h[i] = float(k) * (xm + ym) * self.j[i].det

        p = 0
        for i in range(e.n):
            for j in range(e.n):
                self.H += self.h[p] * self.e.waga[j] * self.e.waga[i]
                p += 1
