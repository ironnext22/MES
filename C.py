from ElementUniwersalny import ElementUniwersalny
from całki import *
from jakobian import Jakobian


class C:
    def __init__(self, e: ElementUniwersalny, cw, rho, det):
        self.cw = cw
        self.rho = rho
        self.det = det
        self.e = e
        self.p = np.zeros([4, e.n, 2])
        self.c = np.zeros([4, 4, 4])
        self.C = np.zeros([4, 4])
        pom = 0
        for i in range(e.n):
            for j in range(e.n):
                N1 = 0.25 * (1 - self.e.tab[i]) * (1 - self.e.tab[j])
                N2 = 0.25 * (1 + self.e.tab[i]) * (1 - self.e.tab[j])
                N3 = 0.25 * (1 + self.e.tab[i]) * (1 + self.e.tab[j])
                N4 = 0.25 * (1 - self.e.tab[i]) * (1 + self.e.tab[j])
                b = np.array([[N1, N2, N3, N4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
                self.c[i] += (self.e.waga[j] * np.matmul(b.T, b) * rho * cw * self.det[pom])
                pom += 1
            self.C += self.c[i]
