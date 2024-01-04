import numpy as np

from C import C
from ElementUniwersalny import ElementUniwersalny
from struktury import *
from całki import *
from jakobian import Jakobian
from Hmatrix import Hmatrix
from HBC import HBC
from P import P
from tovtk import zapis_do_vtk


class licz:
    def __init__(self, grid: Grid, gd: GlobalData, n: int, iterations: int):
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
        self.C = np.zeros([int(gd.Data["Elements number"]), 4, 4])
        self.P = np.zeros([int(gd.Data["Elements number"]), 4])
        self.Hglob = np.zeros([grid.Nodes.size, grid.Nodes.size], dtype=float)
        self.Pglob = np.zeros(grid.Nodes.size, dtype=float)
        self.HC = np.zeros([grid.Nodes.size, grid.Nodes.size], dtype=float)
        self.PC = np.zeros(grid.Nodes.size, dtype=float)
        self.T0 = np.array([float(gd.Data["InitialTemp"]) for i in range(grid.Nodes.size)])
        self.Cglob = np.zeros([grid.Nodes.size, grid.Nodes.size], dtype=float)
        self.solve = np.zeros([iterations + 1, grid.Nodes.size], dtype=float)
        self.solve[0] = self.T0
        self.pc = np.zeros([int(gd.Data["Elements number"]), 4])
        self.iter = iterations

        #obliczanie współrzędnych nodów dla każdego elementu
        self.xe = np.zeros([int(gd.Data["Elements number"]), 4])
        for i in range(int(gd.Data["Elements number"])):
            pom = [self.x[int(a) - 1] for a in self.elements[i].E]
            self.xe[i] = pom

        self.ye = np.zeros([int(gd.Data["Elements number"]), 4])
        for i in range(int(gd.Data["Elements number"])):
            pom = [self.y[int(a) - 1] for a in self.elements[i].E]
            self.ye[i] = pom

        pom = 0

        #obliczanie macierzy H i C dla każdego elementu
        for i in range(int(gd.Data["Elements number"])):
            self.H[i] = Hmatrix(self.xe[i], self.ye[i], self.e, gd.Data["Conductivity"]).H
            self.C[i] = C(self.e, gd.Data["SpecificHeat"], gd.Data["Density"],
                          [Jakobian(self.xe[i], self.ye[i], self.e, j).det for j in range(self.e.n ** 2)]).C

        #obliczanie macierzy HBC i wektora P dla każdego elementu
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
            self.P[i] = P(self.e, gd.Data["Alfa"], det, gd.Data["Tot"], s=pom).P

        self.HBC = np.flip(self.HBC, 0)
        self.P = np.flip(self.P, 0)

        #agregacja macierzy globalnych H i C
        pc = np.zeros([grid.Nodes.size, grid.Nodes.size], dtype=float)
        for i in range(int(gd.Data["Elements number"])):
            pom1 = 0
            p = self.grid.Element[i].E
            for j in p:
                pom2 = 0
                for k in p:
                    self.Hglob[int(j) - 1][int(k) - 1] += self.H[i][pom1][pom2]
                    self.Hglob[int(j) - 1][int(k) - 1] += self.HBC[i][pom1][pom2]
                    self.Cglob[int(j) - 1][int(k) - 1] += self.C[i][pom1][pom2]
                    pom2 += 1
                pom1 += 1
        #obliczanie części równania [H]+ [C]/dtau
        self.HC = self.Hglob + self.Cglob / float(gd.Data["SimulationStepTime"])

        #agragacja wektora globalnego P
        for i in range(int(gd.Data["Elements number"])):
            p = self.grid.Element[i].E
            pom = 0

            for j in p:
                self.Pglob[int(j) - 1] += self.P[i][pom]
                pom += 1

        self.PCpom = np.zeros(grid.Nodes.size, dtype=float)
        #obliczanie części równania ([C]/dtau)*t0 + {P}
        for i in range(iterations):
            self.PC = np.matmul(self.Cglob / float(gd.Data["SimulationStepTime"]), self.solve[i])
            self.PC = self.PC + self.Pglob
            if i == 0: self.PCpom = self.PC
            #obliczanie układu równań
            self.solve[i + 1] = np.linalg.solve(self.HC, self.PC)

        #zapis do pliku
        cells = []
        for i in range(len(self.elements)):
            pom = []
            for j in self.elements[i].E:
                pom.append(j)
            cells.append(pom)

        for i in range(self.solve.shape[0]):
            zapis_do_vtk(self.x, self.y, cells, self.solve[i], f"./vtk/foo{i}.vtk")

    def summary(self, z=7):
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
        print()
        for i in range(int(self.gd.Data["Elements number"])):
            print(f"Macierz C dla elementu {i + 1}: ")
            print(self.C[i])
            print()
        print("Cglob:")
        print(self.Cglob.round(decimals=z))
        print()
        print("HC:")
        print(self.HC.round(decimals=z))
        print()
        print("PC:")
        print(self.PCpom.round(decimals=z))
        print()
        for i in range(self.iter + 1):
            print(f"Solve {i}: ")
            print(self.solve[i].round(decimals=z))
            print(f"Min {np.min(self.solve[i])}, Max {np.max(self.solve[i])}")
            print()


def cd(n1: Node, n2: Node):
    return np.sqrt(np.power(n1.x - n2.x, 2) + np.power(n1.y - n2.y, 2))
