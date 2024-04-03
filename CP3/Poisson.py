import numpy as np
import random
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

def main():
    dx = 1
    e0 = 1
    delta = 0.001  # tolerance value threshold
    #please give system size
    size = int(input())
    nstep = 100000
    
    old_lattice = np.zeros(shape=(size,size,size)) #  set up arbitrary old_lattice
    new_lattice = np.zeros(shape=(size,size,size)) #  set up arbitrary new_lattice

    for n in range(nstep):
        #  old_lattice gets lattice from last update
        old_lattice = np.copy(new_lattice)
        #  update
        new_lattice = jacobi_Algo(old_lattice, dx, size)
        #  checking convergence
        if convergence_checker(new_lattice, old_lattice, delta):
            
            break
    # ------------------------------------------------

    """ Indexing 
        1. potential vs distance
        2. Electric field data
        3. Visualisation
    """
    # 1. ---------------------------------------------
    #  Empty data space for storing potential and distance for plot later
    potential = []
    distance = []

    for i in range(size):
        for j in range(size):
            for k in range(size):
                potential.append(new_lattice[i,j,k])
                distance.append(calc_dist(i,j,k,size))
    #  data writing
#    with open('potential-distance_jacobi.dat', 'w') as f:
#        for pot, dist in zip(distance, potential):
#            f.write(f"{dist}, {pot}\n")

    # 2. ---------------------------------------------
    #  Generating Electric field lattice
    EF_lattice = -1 * E_field(new_lattice,dx)
    data_writer(EF_lattice) # writing out electric field data

    #  empty data space for storing electric field strength and distance
    e_field = []
    for i in range(size):
        for j in range(size):
            for k in range(size):
                e_field.append(EF_lattice[i,j,k])
    #  data writing
    with open('efield-distance_jacobi.dat', 'w') as f:
        for dist, ef in zip(distance, e_field):
            f.write(f"{dist}, {ef}\n")


#  Generating electric field with a dot in a middle of 3D lattice
def E_charge(size):
    lattice = np.zeros(shape=(size,size,size))
    lattice[size//2,size//2,size//2]= 1
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

#  Jacobi Algorithm
def jacobi_Algo(lattice,dx,size):
    lattice = (1/6)*(np.roll(lattice, 1, axis=0)+np.roll(lattice, -1, axis=0)+np.roll(lattice, 1, axis=1)+np.roll(lattice, -1, axis=1)+np.roll(lattice, 1, axis=2)+np.roll(lattice, -1, axis=2)+((dx**2) * E_charge(size)))
    #  Import dirchlet boundary condition
    lattice = dirichlet(lattice)
    return lattice

#  Gauss-Seidel
def Gauss_Algo(new_lattice, dx, size):
    for i in range(size):
        for j in range(size):
            for k in range(size):
                new_lattice[i,j,k] = 1/6 * (new_lattice[(i-1)%size,j,k] + new_lattice[i,(j-1)%size,k] + new_lattice[i,j,(k-1)%size] + new_lattice[(i+1)%size,j,k] + new_lattice[i,(j+1)%size,k] + new_lattice[i,j,(k+1)%size] + ((dx**2) * E_charge(size)))
    # Import dirchlet boundary condition
    new_lattice = dirichlet(new_lattice)
    return new_lattice

#  Vector plot of the electric field
def E_field(potential, dx):
    #  x_axis
    e_right = np.roll(potential,1,axis=2)
    e_left = np.roll(potential,-1,axis=2)
    #  y_axis
    e_up = np.roll(potential,1,axis=1)
    e_down = np.roll(potential,-1,axis=1)
    #  z_axis
    e_upper =np.roll(potential,1,axis=0)
    e_lower =np.roll(potential,-1,axis=0)
    #  discretiation
    x_disc = (1/(2 * dx)) * (e_right - e_left)
    y_disc = (1/(2 * dx)) * (e_up - e_down)
    z_disc = (1/(2 * dx)) * (e_upper - e_lower)

    e_lattice = np.stack((x_disc,y_disc,z_disc), axis=-1)

    return e_lattice

# Distance from center calculator in 3D
def calc_dist(i,j,k,size):
    center_coord = size // 2
    distance = np.sqrt((i - center_coord)**2 + (j - center_coord)**2 + (k - center_coord)**2)
    return distance

#  Successive over relaxation
# def SOR(lattice):

#  checking convergence
def convergence_checker(new_lattice, old_lattice, delta):
    checker = False
    difference = np.sum(abs(new_lattice - old_lattice))
    #print(difference)
    if (difference <= delta):
        checker = True
    return checker

#  data writer
def data_writer(lattice):
    with open('lattice.dat', 'a') as f:
        for row in lattice:
            f.write(' '.join(map(str, row)) + '\n')

#  array printer
def printer(lattice):
    plt.imshow(lattice, cmap='viridis', origin='lower')
    plt.colorbar()  # Add a colorbar to show the color scale
    plt.title('middle slice of potential')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()



#  Printing line
if __name__ == "__main__":
    main()