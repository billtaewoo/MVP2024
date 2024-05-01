import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import csv
import pandas as pd
from tqdm import tqdm

class Canhil:
    def __init__(self, size, pinot, a, k, measurement):
        self.size = size
        self.pinot = pinot
        self.a = a
        self.k = k
        self.measurement = int(measurement)
        # generating the random lattice of given size and phi not
        self.lattice = np.random.uniform(pinot-0.1,pinot+0.1, (self.size,self.size))
    
    # calculating laplacian of given lattice
    def laplacian(self):
        return np.roll(self.lattice, 1,axis=0)+np.roll(self.lattice, -1,axis=0)+np.roll(self.lattice, 1,axis=1)+np.roll(self.lattice, -1,axis=1)-4*self.lattice

    # calculating chemical potential from lattice of phi
    def chemPot(self):
        first_term = self.a * self.lattice
        second_term = self.a * self.lattice ** 3
        third_term =self.k * self.laplacian()
        chPot = -first_term +second_term-third_term
        return chPot
    
    # calculating free energy density, f
    def freeE(self):
        first_term = -(self.a/2)*self.lattice**2
        second_term = (self.a/4)*self.lattice**4
        third_term = (self.k/2)*self.laplacian()**2
        return first_term+second_term+third_term
    #  Calculating explicit Euler algorithm (update function)
    def Euler(self):
        chem = self.chemPot()
        self.lattice += self.a* (np.roll(chem, 1,axis=0)+np.roll(chem, -1,axis=0)+np.roll(chem, 1,axis=1)+np.roll(chem, -1,axis=1)-4*chem)

    # updater
    def animate(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self.lattice, vmin = 0, vmax=1)
        for i in range(self.measurement):
            self.Euler()
            if i % 100 == 0:
                im.set_array(self.lattice)
                plt.pause(0.001)
        plt.show()

def main():
    x = Canhil(50, 0, 0.1, 0.1, 50000)
    y = Canhil(50, 0.5, 0.1, 0.1, 50000)
    x.animate()

main()

