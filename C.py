from ElementUniwersalny import ElementUniwersalny
from całki import *
from jakobian import Jakobian


#Macierz C określa zmianę własności ciała pod wpływem naprężeń/(podwyższenia temperatury)
class C:
    def __init__(self, e: ElementUniwersalny, cw, rho, det):
        self.cw = cw
        self.rho = rho
        self.det = np.array(det)
        self.e = e
        self.c = np.zeros([self.e.n, 4, 4])
        self.C = np.zeros([4, 4])
        pom = 0
        for i in range(e.n):
            for j in range(e.n):
                N1 = 0.25 * (1 - self.e.tab[j]) * (1 - self.e.tab[i])
                N2 = 0.25 * (1 + self.e.tab[j]) * (1 - self.e.tab[i])
                N3 = 0.25 * (1 + self.e.tab[j]) * (1 + self.e.tab[i])
                N4 = 0.25 * (1 - self.e.tab[j]) * (1 + self.e.tab[i])
                b = np.array([[N1, N2, N3, N4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
                self.c[i] += (self.e.waga[j] * self.e.waga[i] * np.matmul(b.T, b) * rho * cw * self.det[pom])
                pom += 1
            self.C += self.c[i]
