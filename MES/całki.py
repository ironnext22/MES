import math
import numpy as np

#2 punkty
#punkty: -sqrt(1/3), sqrt(1/3)
#wagi: 1,1

#3 punkty
#punkty: -sqrt(3/5) , 0 , sqrt(3/5)
#wagi: 5/9, 8/9, 5/9

#4 punkty
#punkty: -0.86113631, -0.33998104,  0.33998104,  0.86113631
#wagi: 0.34785485, 0.65214515, 0.65214515, 0.34785485


class gauss:
    def __init__(self,k):
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





