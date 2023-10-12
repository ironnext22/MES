import numpy as np
import re
class Node:
    def __init__(self,numer:int, x:float , y:float):
        self.numer = numer
        self.x = x
        self.y = y
    def __str__(self):
        return f"{self.x},{self.y}"
    def __repr__(self):
        return repr([self.numer,self.x,self.y])

class Element:
    def __init__(self,numer:int,E:np.array(int)):
        self.numer = numer
        self.E = E
    def __repr__(self):
        return repr(self.E)

class Grid:
    def __init__(self, N:np.array(Node),E:np.array(Element)):
        self.Nodes = N
        self.Element = E

class Dane:
    def __init__(self, path):
        self.filepath = path
        self.data = {}
        self.current_section = None

    def wczytaj(self):
        with open(self.filepath,"r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("*"):
                    self.current_section = line[1:]
                    if self.current_section not in self.data:
                        self.data[self.current_section] = []
                elif self.current_section:
                    values = re.split(r"\s+",line.strip())
                    cv = [float(value.rstrip(",")) for value in values]
                    self.data[self.current_section].append(cv)

    def wpisz_dane(self):
        for section, data in self.data.items():
            print(f"{section}:")
            for i in data:
                print(i)