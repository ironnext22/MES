import numpy as np

from struktury import *
from całki import *

# w = Dane("Test1_4_4.txt")
# w2 = Dane("Test3_31_31_kwadrat.txt")
# w3 = Dane("Test2_4_4_MixGrid.txt")
# grid, gd = w.wczytaj()
# grid2, gd2 = w2.wczytaj()
# grid3, gd3 = w3.wczytaj()
#
# print(grid.Element)
# print()
# print(grid.Nodes)
# print()
# print(gd)
#
# print()

def f(x):
    return 5*x**2+3*x+6

def f2(x,y):
    return 5*x**2*y**2 + 3*x*y + 6

c = gauss(3,1)
print(c.całka(f))
print(c.całka2d(f2))
