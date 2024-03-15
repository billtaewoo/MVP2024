import numpy as np
import random
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

#  Generating random lattice of given size and phi not
def initialization(size, pinot):
    return np.random.uniform(pinot-0.1,pinot+0.1,(size,size))
#  Calculating Laplacian of general square matrix given
def Laplacian(lattice):
   
    return np.roll(lattice, 1,axis=0)+np.roll(lattice, -1,axis=0)+np.roll(lattice, 1,axis=1)+np.roll(lattice, -1,axis=1)-4*lattice

#  Calculating chemical potential from lattice of phi
def chemPot(lattice, a, k):
    first_term = a * lattice
    second_term = a * lattice ** 3
    third_term =k * Laplacian(lattice)
    chPot = -first_term +second_term-third_term
    return chPot
#  Calculating explicit Euler algorithm (update function)
def Euler(lattice, a, k, size):
    chem = chemPot(lattice, a, k)
    dx =1
    dt =1
    lattice += a* (np.roll(chem, 1,axis=0)+np.roll(chem, -1,axis=0)+np.roll(chem, 1,axis=1)+np.roll(chem, -1,axis=1)-4*chem)
    return lattice
# main
def main():
    pinot, a, k, size = map(float, input().split()) # taking variables
    size = int(size)
    lattice = initialization(size, pinot)  # initialized the lattice
    fig = plt.figure()
    im = plt.imshow(lattice,animated=True,vmin=-1,vmax=1)
    nsteps = 1000  # number of steps given

    plt.colorbar()
    for n in tqdm(range(nsteps)):
        lattice = Euler(lattice, a, k, size)  # type a, k and size
        plt.cla()
        im = plt.imshow(lattice, animated=True, vmin=-1, vmax=1)
        plt.draw()
        plt.pause(0.0001)

if __name__ == "__main__":
    main()