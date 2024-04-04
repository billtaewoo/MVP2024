import numpy as np
import random
import scipy.ndimage
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
import scipy

def main():
    dx = 1
    #please give system size
    size = int(input())  # set the system size
    delta = float(input()) # set accuracy of final solution (0.01 or 0.001)
    nstep = 100000
    
    old_lattice = np.zeros(shape=(size,size,size)) #  set up arbitrary old_lattice
    new_lattice = np.zeros(shape=(size,size,size)) #  set up arbitrary new_lattice
    # section for monopole
    for n in range(nstep):
        #  old_lattice gets lattice from last update
        old_lattice = np.copy(new_lattice)
        # update
        new_lattice = jacobi_Algo(old_lattice, dx, size)
        #new_lattice = Gauss_Algo(old_lattice,dx,size)
        #  checking convergence
        if convergence_checker(new_lattice, old_lattice, delta):
            break

    #plt.imshow(new_lattice[size//2,:,:])
    #plt.show()
    # section for wire charge
    '''for n in range(nstep):
        # last lattice become new lattice
        old_lattice = np.copy(new_lattice)
        # update
        new_lattice = jacobi_Algo_wire(old_lattice, dx, size)
        # checking convergence
        if convergence_checker(new_lattice, old_lattice, delta):

            break'''
    # ------------------------------------------------

    """ Indexing 
        1. potential vs distance
        2. Electric field data
        3. Visualisation
    """
# 1. Electric potentil calculation ---------------------------------------------

    potential = []
    distance = []

    '''for i in range(size):
        for j in range(size):
            for k in range(size):
                potential.append(new_lattice[i,j,k])
                distance.append(calc_dist(i,j,k,size))'''
    #  data writing
#    with open('potential-distance_jacobi.dat', 'w') as f:
#        for pot, dist in zip(distance, potential):
#            f.write(f"{dist}, {pot}\n")

# 2. Electric field strength calculation ---------------------------------------------
    Ef_lattice = E_field(new_lattice)  #returns the 3D lattice of electric field strength
    Efstrength = []
    
   
# 3. Electric field vector calculation in the middle slice-----------------------------------------
    x_arrow, y_arrow = E_vector(new_lattice,size)
    x = np.arange(0, size, 1)
    y = np.arange(0, size, 1)
    x_1, y_1 = np.meshgrid(x,y)
    x_2 = x_1.flatten()
    y_2 = y_1.flatten()

    fig, ax =plt.subplots(figsize = (12,7))
    ax.quiver(x_2,y_2,x_arrow,y_arrow,scale=0.5)
    plt.show()

# -------------------------------END OF MAIN-----------------------------------------------------------
# CHARGE TYPES ----------------------------------------------------------------------------------------
#  Generating electric field with a dot in a middle of 3D lattice
def monopole(size):
    lattice = np.zeros(shape=(size,size,size))
    lattice[size//2,size//2,size//2]= 1
    return lattice

#  Generating electric wire in 3D empty space (this is for Magnetic potential calculation)
def wire_origin(size):
    lattice = np.zeros(shape=(size,size,size))  # generate the empty cubic space by given size
    #  wire is align with z axis and running through origin.
    lattice[:, size//2, size//2] = 1
    return lattice

#  ALGORITHMS-------------------------------------------------------------------------------------------

#  Jacobi Algorithm for point charge
def jacobi_Algo(lattice,dx,size):
    latticecopy = np.copy(lattice)
    n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
    latticecopy = (1/6) * ((scipy.ndimage.convolve(latticecopy, n, mode='constant',cval=0) + ((dx**2) * monopole(size))))
    return latticecopy

#  Jacobi Algorithm for wire (MAGNETIC FIELD CALCULATION)
def jacobi_Algo_wire(lattice,dx,size):
    latticecopy = np.copy(lattice)
    n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
    latticecopy = (1/6) * ((scipy.ndimage.convolve(latticecopy, n, mode='constant',cval=0) + ((dx**2) * wire_origin(size))))
    return latticecopy

#  Gauss-Seidel for point charge
def Gauss_Algo(lattice, dx, size):
    #making checker board
    latticecopy = np.copy(lattice)
    checker = np.sum(np.indices(lattice.shape),axis = 0) % 2
    #making neighbour array for convolution
    n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]) # object represent laplacian
    # update
    latticecopy[checker == 1] = (1/6) * ((scipy.ndimage.convolve(latticecopy, n, mode='constant',cval=0) + ((dx**2) * monopole(size))))[checker == 1]
    latticecopy[checker == 0] = (1/6) * ((scipy.ndimage.convolve(latticecopy, n, mode='constant',cval=0) + ((dx**2) * monopole(size))))[checker == 0]
    return latticecopy

#  Successive over-relaxation (FOR GAUSS-SEIDEL ALGORITHM)
def SOR(new_lattice, old_lattice, w):
    #  Set difference between new lattice and old lattice
    dp = new_lattice - old_lattice
    #  Set relaxation parameter must be 1 < w < 2
    sor_lat = new_lattice + w * dp
    return sor_lat

# MISCELLANIOUS CALCULATORS -----------------------------------------------------------------------------
#  calculate electric field strength
def E_field(potential):
    copypotential = np.copy(potential)
    n = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[-1,0,1],[0,-1,0]],[[0,0,0],[0,-1,0],[0,0,0]]]) # object represent grad
    copypotential = -1 * (1/6) * (scipy.ndimage.convolve(copypotential, n, mode='constant',cval=0))
    return copypotential
#  calculate electric field vectors
def E_vector(potential,size):
    copypotential = np.copy(potential)
    middleslice = copypotential[size//2,:,:] # take the middle slice of 3D potential
    xn = np.array([[0,0,0],[-1,0,1],[0,0,0]]) # grad of x component
    yn = np.array([[0,1,0],[0,0,0],[0,-1,0]]) # grad of y component
    dx = 1/2 * (scipy.ndimage.convolve(middleslice,xn,mode='constant',cval=0))
    dy = -1/2 * (scipy.ndimage.convolve(middleslice,yn,mode='constant',cval=0))
    delx = dx.flatten()
    dely = dy.flatten()
    return delx, dely  # returns list of electric field vector






# Distance from center calculator in 3D
def calc_dist(i,j,k,size):
    center_coord = size // 2
    distance = np.sqrt((i - center_coord)**2 + (j - center_coord)**2 + (k - center_coord)**2)
    return distance

#  checking convergence
def convergence_checker(new_lattice, old_lattice, delta):
    checker = False
    difference = np.sum(abs(new_lattice - old_lattice))
    #print(difference)
    if (difference <= delta):
        checker = True
    return checker

# DATA WRITTERS ------------------------------------------------------------------------------
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

# END OF FUNCTION LINES -----------------------------------------------------------------------

#  Printing line
if __name__ == "__main__":
    main()