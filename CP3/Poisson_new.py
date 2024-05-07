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
        self.type = type
        if type == "monopole":
            if dim == 2:
                self.lattice = np.zeros(shape=(self.size, self.size))
                self.lattice[self.size//2, self.size//2] = 1
                self.mono[self.size//2, self.size//2] = 1
            elif dim == 3:
                self.lattice = np.zeros(shape=(self.size, self.size, self.size))
                self.lattice[self.size//2, self.size//2, self.size//2] = 1
                self.mono[self.size//2, self.size//2, self.size//2] = 1
        elif type == "wire":
            if dim == 2:
                self.lattice = np.zeros(shape=(self.size,self.size))
                self.lattice[self.size//2, self.size//2] = 1
                self.wire[self.size//2, self.size//2] = 1
            elif dim ==3:
                self.lattice = np.zeros(shape=(self.size,self.size))
                self.lattice[:, self.size//2, self.size//2] = 1
                self.wire[:, self.size//2, self.size//2] = 1

    def jacobi_Algo(self): #dim 2 is not ready
        if self.type == "monopole":
            if self.dim == 3:
                filters = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
                self.lattice = (1/6) * ((scipy.ndimage.convolve(self.lattice, filters, mode='constant',cval=0) + self.mono))
        elif self.type == "wire":
            if self.dim == 3:
                filters = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
                self.lattice = (1/6) * ((scipy.ndimage.convolve(self.lattice, filters, mode='constant',cval=0) + self.wire))

    def Gauss_Algo(self):
        if self.type == "monopole":
            if self.dim == 3:
                #making checker board
                checker = np.sum(np.indices(self.lattice.shape),axis = 0) % 2
                #making neighbour array for convolution
                n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
                # update
                self.lattice[checker == 1] = (1/6) * ((scipy.ndimage.convolve(self.lattice, n, mode='constant',cval=0) + self.mono))[checker == 1]
                self.lattice[checker == 0] = (1/6) * ((scipy.ndimage.convolve(self.lattice, n, mode='constant',cval=0) + self.mono))[checker == 0]
        elif self.type == "wire":
            if self.dim == 3:
                #making checker board
                checker = np.sum(np.indices(self.lattice.shape),axis = 0) % 2
                #making neighbour array for convolution
                n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
                # update
                self.lattice[checker == 1] = (1/6) * ((scipy.ndimage.convolve(self.lattice, n, mode='constant',cval=0) + self.wire))[checker == 1]
                self.lattice[checker == 0] = (1/6) * ((scipy.ndimage.convolve(self.lattice, n, mode='constant',cval=0) + self.wire))[checker == 0]
    # successive over-relaxation for gauss seidel algorithm
    def SOR(self, w):
        # w = np.arange(1.0, 2.01, 0.01) #list of w (Relax parameter)
        prev = np.copy(self.lattice)
        checker = np.sum(np.indices(self.lattice.shape),axis = 0) % 2
        #making neighbour array for convolution
        n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
        # update
        self.lattice[checker == 1] = (1/6) * ((scipy.ndimage.convolve(self.lattice, n, mode='constant',cval=0) + self.wire))[checker == 1]
        self.lattice = w * self.lattice + (1-w) * prev
        self.lattice[checker == 0] = (1/6) * ((scipy.ndimage.convolve(lattice, n, mode='constant',cval=0) + self.wire))[checker == 0]
        self.lattice = w * self.lattice + (1-w) * prev

    def E_field(self):
        if self.dim==3:
            dx = -0.5 * (np.roll(self.lattice,1,axis=0)-np.roll(self.lattice,-1,axis=0) )[1:self.size,1:self.size,self.size//2].ravel()
            dy = -0.5 * (np.roll(self.lattice,1,axis=1)-np.roll(self.lattice,-1,axis=1) )[1:self.size,1:self.size,self.size//2].ravel()
            dz = -0.5 * (np.roll(self.lattice,1,axis=2)-np.roll(self.lattice,-1,axis=2) )[1:self.size,1:self.size,self.size//2].ravel()
            return dx, dy, dz

