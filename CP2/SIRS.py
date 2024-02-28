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
            if 