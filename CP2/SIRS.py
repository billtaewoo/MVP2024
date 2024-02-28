import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import random
from tqdm import tqdm
from matplotlib import pyplot as plt

'''
    S : susceptible to the infection (0)
    I : infected                     (1)   
    R : recovered from the infection (2)
'''

def initialize(size):
    # part for generate the random array of given size
    return np.random.choice([0, 1, 2], size=(size, size))

def SIR(size, array, prob1, prob2, prob3):
    # If at least 1 neighbour is infected, update to I. If not S.
    original = array  # copy original
    copy = np.zeros(shape=(size,size))  # empty copy get update
    for i in range(size):
        for j in range(size):
            x = original[i][j] # get update point
            if x == 0:
                if random.random() < prob1:  # checking probability 1
                    if original[(i-1)%size][j] == 1:  # left
                        original[i][j] = 1 
                        copy[i][j] = 1
                    elif original[(i+1)%size][j] == 1:  # right
                        original[i][j] = 1 
                        copy[i][j] = 1
                    elif original[i][(j-1)%size] == 1:  # up
                        original[i][j] = 1 
                        copy[i][j] = 1
                    elif original[i][(j+1)%size] == 1:  # down
                        original[i][j] = 1 
                        copy[i][j] = 1
                    else:
                        pass
                else:
                    pass
            # if update point is infected take recovery action
            elif x == 1:
                if random.random() < prob2:
                    original[i][j] = 2
                    copy[i][j] = 2
                else:
                    pass
            # if update point is recovered form infection take susceptible action
            elif x == 2:
                if random.random() < prob3:
                    original[i][j] = 0
                    copy[i][j] = 0
                else:
                    pass
            else:
                pass
    return copy  # return the updated array

'''
End of the functions.
'''

def main():
    size, prob1, prob2, prob3 = map(float, input().split()) # taking variables
    size = int(size)
    lattice = initialize(size)  # initialized the lattice
    nsteps = 100  # number of steps given
    for n in tqdm(range(nsteps)):
        lattice = SIR(size, lattice, prob1, prob2, prob3)
        
        plt.cla()
        im = plt.imshow(lattice, animated=True)
        plt.draw()
        plt.pause(0.0001)

if __name__ == "__main__":
    main()