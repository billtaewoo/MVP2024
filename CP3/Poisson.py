import numpy as np
import random
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

def main():
    dx = 1
    e0 = 1

def initialization():
    return np.
#  Calculating 3D Laplacian of general square matrix given
def Laplacian(lattice):
    return np.roll(lattice, 1,axis=0)+np.roll(lattice, -1,axis=0)+np.roll(lattice, 1,axis=1)+np.roll(lattice, -1,axis=1)+np.roll(lattice, 1, axis=2)+np.roll(lattice, -1, axis=2)-6*lattice
#  Calculating Field of Electric charge
def E_charge(lattice,e0):
    return -1 * e0 * Laplacian(lattice)
#  Jacobi Algorithm
def jacobi_Algo(lattice,dx,e0):
    lattice += (1/6)*(np.roll(lattice, 1, axis=0)+np.roll(lattice, -1, axis=0)+np.roll(lattice, 1, axis=1)+np.roll(lattice, -1, axis=1)+np.roll(lattice, 1, axis=2)+np.roll(lattice, -1, axis=2)+((dx**2)*E_charge(lattice,e0)))
    return lattice
#  Gauss-Seidel
def Gauss_Algo(lattice,dx,e0):
    
#  Printing line
if __name__ == "__main__":
    main()