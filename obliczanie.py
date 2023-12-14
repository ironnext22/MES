import numpy as np
from ElementUniwersalny import ElementUniwersalny
from struktury import *
from całki import *
from jakobian import Jakobian
from Hmatrix import Hmatrix
from HBC import HBC
from P import P


class licz:
    def __init__(self, grid: Grid, gd: GlobalData, n: int):
        self.grid = grid
        self.gd = gd
        self.e = ElementUniwersalny(n)
        XY = grid.Nodes
        self.x = [i.x for i in XY]
        self.y = [i.y for i in XY]
        self.elements = self.grid.Element
        self.H = np.zeros([int(gd.Data["Elements number"]), 4, 4])
        self.HBC = np.zeros([int(gd.Data["Elements number"]), 4, 4])
        self.HWB = np.zeros([int(gd.Data["Elements number"]), 4, 4])
        self.P = np.zeros([int(gd.Data["Elements number"]), 4])
        self.Hglob = np.zeros([grid.Nodes.size, grid.Nodes.size], dtype=float)
        self.Pglob = np.zeros(grid.Nodes.size, dtype=float)

        self.xe = np.zeros([int(gd.Data["Elements number"]), 4])
        for i in range(int(gd.Data["Elements number"])):
            pom = [self.x[int(a) - 1] for a in self.elements[i].E]
            self.xe[i] = pom

        self.ye = np.zeros([int(gd.Data["Elements number"]), 4])
        for i in range(int(gd.Data["Elements number"])):
            pom = [self.y[int(a) - 1] for a in self.elements[i].E]
            self.ye[i] = pom

        for i in range(int(gd.Data["Elements number"])):
            self.H[i] = Hmatrix(self.xe[i], self.ye[i], self.e, gd.Data["Conductivity"]).H

        for i in range(int(gd.Data["Elements number"])):
            pom = []
            k = np.array([self.elements[i].E[2], self.elements[i].E[1], self.elements[i].E[0], self.elements[i].E[3]])
            det = []
            for j in range(k.size):
                p = j + 1
                if p == k.size: p = 0
                if np.any(gd.BC == k[j]) and np.any(gd.BC == k[p]): pom.append(j)
                det.append(cd(self.grid.Nodes[int(k[j]) - 1], self.grid.Nodes[int(k[p] - 1)]) / 2)
            self.HBC[i] = HBC(self.e, gd.Data["Alfa"], det, s=pom).HBC
            self.P[i] = P(self.e, gd.Data["Alfa"], det, 1200, s=pom).P

        self.HBC = np.flip(self.HBC, 0)
        self.P = np.flip(self.P, 0)

        # print(self.H.shape[0])
        # print(self.grid.Element[0])
        for i in range(int(gd.Data["Elements number"])):
            pom1 = 0
            print(i)
            p = self.grid.Element[i].E
            print(p)
            for j in p:
                pom2 = 0
                for k in p:
                    self.Hglob[int(j) - 1][int(k) - 1] += self.H[i][pom1][pom2]
                    self.Hglob[int(j) - 1][int(k) - 1] += self.HBC[i][pom1][pom2]
                    pom2 += 1
                pom1 += 1

        for i in range(int(gd.Data["Elements number"])):
            p = self.grid.Element[i].E
            pom = 0
            for j in p:
                self.Pglob[int(j) - 1] += self.P[i][pom]
                pom += 1

        # for i in range(int(gd.Data["Elements number"])):
        #     self.HWB[i] = self.H[i] + self.HBC[i]

    def summary(self,z=7):
        for i in range(int(self.gd.Data["Elements number"])):
            print(f"Macierz H dla elementu {i + 1}: ")
            print(self.H[i])
            print()
        for i in range(int(self.gd.Data["Elements number"])):
            print(f"Macierz HBC dla elementu {i + 1}: ")
            print(self.HBC[i])
            print()
        for i in range(int(self.gd.Data["Elements number"])):
            print(f"Wektor P dla elementu {i + 1}: ")
            print(self.P[i])
            print()
        print("Hglob:")
        print(self.Hglob.round(decimals=z))
        print("Pglob:")
        print(self.Pglob.round(decimals=z))
        # for i in range(int(self.gd.Data["Elements number"])):
        #     print(f"Macierz HWB dla elementu {i + 1}: ")
        #     print(self.HWB[i])
        #     print()


def cd(n1: Node, n2: Node):
    return np.sqrt(np.power(n1.x - n2.x, 2) + np.power(n1.y - n2.y, 2))
