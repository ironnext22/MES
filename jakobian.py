import numpy as np
from ElementUniwersalny import ElementUniwersalny


class Jakobian:
    def __init__(self, x: [], y: [], e: ElementUniwersalny, punkt: int = 0):
        self.x = np.array(x)
        self.y = np.array(y)
        self.dX_DKsi = np.sum([self.x[i] * e.dNKsi[punkt][i] for i in range(np.size(self.x))])
        self.dX_DEta = np.sum([self.x[i] * e.dNEta[punkt][i] for i in range(np.size(self.x))])
        self.dY_DKsi = np.sum([self.y[i] * e.dNKsi[punkt][i] for i in range(np.size(self.x))])
        self.dY_DEta = np.sum([self.y[i] * e.dNEta[punkt][i] for i in range(np.size(self.x))])

        self.jac = np.array([[self.dX_DKsi, self.dY_DKsi], [self.dX_DEta, self.dY_DEta]])
        self.det = np.linalg.det(self.jac)
        self.inv = 1 / self.det * np.array([[self.dY_DEta, -self.dY_DKsi], [-self.dX_DEta, self.dX_DKsi]])
        # self.inv = np.linalg.inv(self.jac)
