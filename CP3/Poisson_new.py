import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import csv
import pandas as pd
from tqdm import tqdm

class Poisson:
    def __init__(self, size, type, dim, measurements):
        self.size = size
        self.measurement = measurements
        self.dim = dim
        if type == "monopole":
            if dim == 2:
                self.lattice = np.zeros(shape=(self.size, self.size))
                self.lattice[self.size//2, self.size//2] = 1
            elif dim == 3:
                self.lattice = np.zeros(shape=(self.size, self.size, self.size))
                self.lattice[self.size//2, self.size//2, self.size//2] = 1
        elif type == "wire":
            if dim == 2:
                self.lattice = np.zeros(shape=(self.size,self.size))
                self.lattice[self.size//2, self.size//2] = 1
            elif dim ==3:
                self.lattice = np.zeros(shape=(self.size,self.size))
                self.lattice[:, self.size//2, self.size//2] = 1

    def jacobi_Algo(self):
        if self.dim == 3:
            filters = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
            self.lattice = (1/6) * ((scipy.ndimage.convolve(self.lattice, filters, mode='constant',cval=0) + ( self.lattice)))
