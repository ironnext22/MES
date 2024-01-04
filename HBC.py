from ElementUniwersalny import ElementUniwersalny
from struktury import *
from całki import *
from jakobian import Jakobian
from Hmatrix import Hmatrix
import numpy as np



class HBC:
    def __init__(self, e: ElementUniwersalny, alfa, det, s=None):
        if s is None:
            s = [0, 1, 2, 3]
        self.alfa = alfa
        # self.det = det
        self.det = np.array(det)
        self.e = e
        self.hbc = np.zeros([4, 4, 4])
        self.p = np.zeros([4, e.n, 2])
        self.HBC = np.zeros([4, 4])
        self.pom = np.zeros([e.n, 2])
        for i in range(e.n):
            self.pom[i] = [-1, e.tab[i]]
        self.p[0] = self.pom
        for i in range(e.n):
            self.pom[i] = [e.tab[i], 1]
        self.p[1] = self.pom
        for i in range(e.n):
            self.pom[i] = [1, e.tab[i]]
        self.p[2] = self.pom
        for i in range(e.n):
            self.pom[i] = [e.tab[i], -1]
        self.p[3] = self.pom

        for i in s:
            for j in range(e.n):
                N1 = 0.25 * (1 - self.p[i][j][0]) * (1 - self.p[i][j][1])
                N2 = 0.25 * (1 + self.p[i][j][0]) * (1 - self.p[i][j][1])
                N3 = 0.25 * (1 + self.p[i][j][0]) * (1 + self.p[i][j][1])
                N4 = 0.25 * (1 - self.p[i][j][0]) * (1 + self.p[i][j][1])
                b = np.array([[N1, N2, N3, N4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
                self.hbc[i] += (self.e.waga[j] * np.matmul(b.T, b) * alfa)
            self.hbc[i] *= self.det[i]
            self.HBC += self.hbc[i]