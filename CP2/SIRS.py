import numpy as np
from tqdm import tqdm

'''
    S : susceptible to the infection (0)
    I : infected                     (1)   
    R : recovered from the infection (2)
'''

def initialize(size):
    # part for generate the random array of given size
    return np.random.choice([0, 1, 2], size=(size, size))

def infection(size, array, prob1):
    # If at least 1 neighbour is infected, update to I. If not S.
    original = array  # copy original
    copy = np.zeros(shape=(size,size))  # empty copy get update
    for i in range(size):
        for j in range(size):
            x = original[i][j] # get update point
            if x == 0:
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
                pass  # just pass if point is not infected (1)
    return copy  # return the updated array
