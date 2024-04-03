import numpy as np
import random
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

def main():
    dx = 1
    e0 = 1
    size = 50

#  Generating empty lattice with a dot in a middle of 3D lattice
def point_charge_init(size):
    lattice = np.zeros(shape=(size,size,size))
    lattice[size/2][size/2][size/2]= 1
    return lattice

#  Set up the dirichlet boundary condition (3D)
def dirichlet(lattice):
    lattice[0, :, :] = 0
    lattice[:, 0, :] = 0
    lattice[:, :, 0] = 0
    lattice[-1, :, :] = 0
    lattice[:, -1, :] = 0
    lattice[:, :, -1] = 0
    return lattice

#  Calculating 3D Laplacian of general square matrix given
def Laplacian(lattice):
    return np.roll(lattice, 1,axis=0)+np.roll(lattice, -1,axis=0)+np.roll(lattice, 1,axis=1)+np.roll(lattice, -1,axis=1)+np.roll(lattice, 1, axis=2)+np.roll(lattice, -1, axis=2)-6*lattice

#  Calculating Field of Electric charge
def E_charge(lattice,e0):
    return -1 * e0 * Laplacian(lattice)

#  Jacobi Algorithm
def jacobi_Algo(old_lattice,dx,e0):
    new_lattice += (1/6)*(np.roll(old_lattice, 1, axis=0)+np.roll(old_lattice, -1, axis=0)+np.roll(old_lattice, 1, axis=1)+np.roll(old_lattice, -1, axis=1)+np.roll(old_lattice, 1, axis=2)+np.roll(old_lattice, -1, axis=2)+((dx**2)*E_charge(old_lattice,e0)))
    #  import dirchlet boundary condition
    new_lattice = dirichlet(new_lattice)
    return new_lattice

#  Gauss-Seidel
def Gauss_Algo(new_lattice,dx,e0):
    # only gets new lattice!
    new_lattice += (1/6)*(np.roll(new_lattice, 1, axis=0)+np.roll(new_lattice, -1, axis=0)+np.roll(new_lattice, 1, axis=1)+np.roll(new_lattice, -1, axis=1)+np.roll(new_lattice, 1, axis=2)+np.roll(new_lattice, -1, axis=2)+((dx**2)*E_charge(new_lattice,e0)))
    # Import dirchlet boundary condition
    new_lattice = dirichlet(new_lattice)
    return new_lattice

#  checking convergence
def convergence_checker(new_lattice, old_lattice, delta):
    checker = False
    difference = np.sum(abs(new_lattice - old_lattice))
    if (difference <= delta):
        checker = True
    return checker

#  Printing line
if __name__ == "__main__":
    main()