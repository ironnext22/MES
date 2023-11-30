import numpy as np
from ElementUniwersalny import ElementUniwersalny
from struktury import *
from całki import *
from jakobian import Jakobian
from Hmatrix import Hmatrix
from obliczanie import licz
from HBC import HBC

w = Dane("Test1_4_4.txt")
w2 = Dane("Test3_31_31_kwadrat.txt")
w3 = Dane("Test2_4_4_MixGrid.txt")
grid, gd = w.wczytaj()
grid2, gd2 = w2.wczytaj()
grid3, gd3 = w3.wczytaj()
#
# print(grid.Element)
# print()
# print(grid.Nodes)
# print()
# print(gd)
#
# print()

# def f(x):
#     return 5*x**2+3*x+6
#
# def f2(x,y):
#     return 5*x**2*y**2 + 3*x*y + 6

# c = gauss(3,1)
# print(c.całka(f))
# print(c.całka2d(f2))
#
# w = ElementUniwersalny(3)
#
# print("dNEta: \n")
# print(w.dNEta)
# print("\n")
# print("dNKsi: \n")
# print(w.dNKsi)

print(np.polynomial.legendre.leggauss(3))
XY = grid.Nodes
# print(XY)

x = [0, 0.025, 0.025, 0]
y = [0, 0, 0.025, 0.025]
e = ElementUniwersalny(2)
# j = Jakobian(x,y,e)
#
# # print(j.jac)
# # print(j.inv)
#
# h = Hmatrix(x,y,e)
# print(h.H)

XY = grid3.Nodes
# x = np.array([1,2,3])[np.newaxis]
# print(x)
# print(x.T)
x = [i.x for i in XY]
y = [i.y for i in XY]
xpom = [x[0], x[1], x[5], x[4]]
ypom = [y[0], y[1], y[5], y[4]]
j = Jakobian(xpom, ypom, e, 0)
h = Hmatrix(xpom, ypom, e, gd.Data["Conductivity"])
# print(j.inv)
# print(h.dNidx)
# print(h.H)

l = licz(grid3, gd3, 2)

l.summary()

# h = HBC(e, 25, 0.0125)
# print(h.HBC)
