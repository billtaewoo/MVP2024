from matplotlib import pyplot as plt
import numpy as np
import scipy

class lattice:
    def __init__(self, size) -> None:
        self.size = size
    def random(self):
        self.lattice = np.random.choice([0, 1], size=(self.size, self.size))
    def oscillator(self):
        lattice = np.zeros((self.size,self.size))
        x = np.random.randint(self.size)
        y = np.random.randint(self.size)
        if lattice[y,x] == 0:
            lattice[y,x] = 1
            lattice[y,(x-1)%self.size] = 1
            lattice[y,(x+1)%self.size] = 1
            self.lattice = lattice
    def glider(self):
        lattice = np.zeros((self.size,self.size))
        x = np.random.randint(self.size)
        y = np.random.randint(self.size)
        if lattice[y,x] == 0:
            lattice[(y-1)%self.size][x] = 1
            lattice[y][(x+1)%self.size] = 1
            lattice[(y+1)%self.size][(x+1)%self.size] = 1
            lattice[(y+1)%self.size][x] = 1
            lattice[(y+1)%self.size][(x-1)%self.size] = 1
            self.lattice = lattice
    
class GameofLife(lattice):
    def update(self):
        empty = np.zeros((self.size,self.size))
        neighbour = empty + np.roll(self.lattice,1,axis= 0) + np.roll(self.lattice,-1,axis=0) + np.roll(self.lattice, 1, axis= 1) + np.roll(self.lattice, -1, axis=1)

        