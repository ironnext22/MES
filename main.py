from struktury import *
from obliczanie import licz

w = Dane("Test1_4_4.txt")
w2 = Dane("Test3_31_31_kwadrat.txt")
w3 = Dane("Test2_4_4_MixGrid.txt")
w4 = Dane("Test4_31_31_trapez.txt")
grid, gd = w.wczytaj()
grid2, gd2 = w2.wczytaj()
grid3, gd3 = w3.wczytaj()
grid4, gd4 = w4.wczytaj()

oblicz = licz(grid3, gd3, 4, 10)

oblicz.summary(3)
