import math
import numpy as np


class gauss:
    def __init__(self,k,d):
        self.k = k
        self.x, self.w = np.polynomial.legendre.leggauss(self.k)
    def całka(self,f):
        a,b = -1,1
        return ((b-a)/2)*np.sum(self.w*f((b-a)/2*self.x+(a+b)/2))

    def całka2d(self,f):
        integral = 0
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                integral += self.w[i]*self.w[j]*f(self.x[i],self.x[j])
        return integral
        #return np.sum(np.outer(self.w, self.w) * f(np.outer(self.x, np.ones_like(self.x)), np.outer(np.ones_like(self.x), self.x)))





