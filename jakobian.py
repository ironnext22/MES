import numpy as np
def dN1ksi(eta):
    return -1/4*(1-eta)
def dN2ksi(eta):
    return 1/4*(1-eta)
def dN3ksi(eta):
    return 1/4*(1-eta)
def dN4ksi(eta):
    return -1/4*(1-eta)

def dN1eta(ksi):
    return -1/4*(1-ksi)
def dN2eta(ksi):
    return -1/4*(1-ksi)
def dN3eta(ksi):
    return 1/4*(1-ksi)
def dN4eta(ksi):
    return 1/4*(1-ksi)




class ElementUniwersalny:
    def __init__(self, n:int):
        self.tab = np.polynomial.legendre.leggauss(n)[0]
        self.dNKsi = np.zeros([4, n**2])
        self.dNEta = np.zeros([4, n**2])
        self.pom = 0
        for i in range(n**2):
            if (i != 0 and i % n == 0): self.pom += 1
            self.dNKsi[i][0] = dN4ksi(self.tab[self.pom])
        self.pom = 0
        for i in range(n**2):
            if (i != 0 and i % n == 0): self.pom += 1
            self.dNKsi[i][1] = dN3ksi(self.tab[self.pom])
        self.pom = n-1
        for i in range(n**2):
            if(i!=0 and i%n==0): self.pom -= 1
            self.dNKsi[i][2] = dN2ksi(self.tab[self.pom])
        self.pom = n-1
        for i in range(n**2):
            if(i!=0 and i%n==0): self.pom -= 1
            self.dNKsi[i][3] = dN1ksi(self.tab[self.pom])
        self.pom = 0

        for i in range(n**2):
            self.pom = i%n
            #if (i != 0 and i % n == 0): self.pom += 1
            self.dNEta[i][0] = dN1eta(self.tab[self.pom])
        for i in range(n**2):
            self.pom = i % n
            #if (i != 0 and i % n == 0): self.pom += 1
            self.dNEta[i][1] = dN2eta(self.tab[self.pom])
        for i in range(n**2):
            self.pom = i % n
            #if(i!=0 and i%n==0): self.pom -= 1
            self.dNEta[i][2] = dN3eta(self.tab[self.pom])
        for i in range(n**2):
            self.pom = i % n
            #if(i!=0 and i%n==0): self.pom -= 1
            self.dNEta[i][3] = dN4eta(self.tab[self.pom])