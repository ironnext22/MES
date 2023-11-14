import numpy as np
from ElementUniwersalny import ElementUniwersalny
from struktury import *
from całki import *
from jakobian import Jakobian
from Hmatrix import Hmatrix


class licz:
    def __init__(self, grid: Grid, gd: GlobalData, n: int):
        self.grid = grid
        self.gd = gd
        self.e = ElementUniwersalny(n)
        XY = grid.Nodes
        self.x = [i.x for i in XY]
        self.y = [i.y for i in XY]
        self.elements = self.grid.Element
        self.H = np.zeros([int(gd.Data["Elements number"]),4,4])

        self.xe = np.zeros([int(gd.Data["Elements number"]),4])
        for i in range(int(gd.Data["Elements number"])):
            pom = [self.x[int(a)-1] for a in self.elements[i].E]
            self.xe[i] = pom

        self.ye = np.zeros([int(gd.Data["Elements number"]),4])
        for i in range(int(gd.Data["Elements number"])):
            pom = [self.y[int(a)-1] for a in self.elements[i].E]
            self.ye[i] = pom

        for i in range(int(gd.Data["Elements number"])):
            self.H[i] = Hmatrix(self.xe[i],self.ye[i],self.e,gd.Data["Conductivity"]).H


    def summary(self):
        for i in range(int(self.gd.Data["Elements number"])):
            print(f"Macierz H dla elementu {i+1}: ")
            print(self.H[i])
            print()
