import numpy as np
import re


class GlobalData:
    def __init__(self, data: dict, BC: []):
        self.Data = data
        self.BC = np.array(BC)

    def __repr__(self):
        return repr(self.Data)


class Node:
    def __init__(self, numer: int, x: float, y: float):
        self.numer = numer
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x},{self.y}\n"

    def __repr__(self):
        return repr([self.numer, self.x, self.y])


class Element:
    def __init__(self, numer: int, E):
        self.numer = numer
        self.E = np.array(E)

    def __repr__(self):
        return repr(self.E)


class Grid:
    def __init__(self, N: [Node], E: [Element]):
        self.Nodes = np.array(N)
        self.Element = np.array(E)


class Dane:
    def __init__(self, path):
        self.filepath = path
        self.data = {}
        self.data2 = {}
        self.current_section = None

    def wczytaj3(self):
        with open(self.filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("*"):
                    self.current_section = line[1:]
                    if self.current_section not in self.data:
                        self.data[self.current_section] = []
                elif self.current_section:
                    values = re.split(r"\s+", line.strip())
                    cv = [float(value.rstrip(",")) for value in values]
                    self.data[self.current_section].append(cv)
        file.close()

    def wczytaj2(self):
        with open(self.filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("*"): break
                values = re.split(r"\s", line.strip())
                if values[0] == "Elements" or values[0] == "Nodes":
                    self.data2[values[0] + " " + values[1]] = float(values[2])
                else:
                    self.data2[values[0]] = float(values[1])
        file.close()
        return self.data2

    def wczytaj(self):
        self.wczytaj3()
        t = self.data["Node"]
        t2 = self.data["Element, type=DC2D4"]
        pomnode = []
        pomelement = []

        for i in t:
            pomnode.append(Node(i[0], i[1], i[2]))
        for i in t2:
            pomelement.append(Element(i[0], i[1:]))

        grid = Grid(pomnode, pomelement)
        glob = GlobalData(self.wczytaj2(), self.data["BC"])

        return grid, glob

    def wpisz_dane(self):
        for section, data in self.data.items():
            print(f"{section}:")
            for i in data:
                print(i)
