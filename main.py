from struktury import *


w = Dane("Test1_4_4.txt")
w.wczytaj()
#print(w.data["Node"])

t = w.data["Node"]
t2 = w.data["Element, type=DC2D4"]
pomnode = []
pomelement = []

for i in t:
    pomnode.append(Node(i[0], i[1], i[2]))
for i in t2:
    pomelement.append(Element(i[0],i[1:]))

grid = Grid(pomnode,pomelement)
print(grid.Element)
