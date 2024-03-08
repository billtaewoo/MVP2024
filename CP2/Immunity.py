import numpy as np
import random
from tqdm import tqdm

'''
    S : susceptible to the infection (0)
    I : infected                     (1)   
    R : recovered from the infection (2)
    Im : Immuned                     (3)

    '''

def initialize(size):
    # part for generate the random array of given size
    return np.random.choice([0, 1, 2], size=(size, size))

def Immun_generator(size, array, Im):
    Im_num = int((size * size)*Im)  # give number of immuned pop
    lattice = array  # lattice of pops
    for n in range(Im_num+1):
        i = int(random.random()*size)
        j = int(random.random()*size)
        while lattice[i][j] == 3:
            i = int(random.random()*size)
            j = int(random.random()*size)
        lattice[i][j] = 3  # make it immune
    return lattice
        
def SIR(size, array, prob1, prob2, prob3):

    original = array  # copy original

    i = int(random.random()*size)
    j = int(random.random()*size)
    x = original[i][j] # get update point
    if x == 0:
        if original[(i-1)%size][j] == 1:
            if random.random() <= prob1:  # checking probability 1
                original[i][j] = 1
            else:
                pass
        elif original[(i+1)%size][j] == 1:
            if random.random() <= prob1:  # checking probability 1
                original[i][j] = 1
            else:
                pass
        elif original[i][(j-1)%size] == 1:
            if random.random() <= prob1:  # checking probability 1
                original[i][j] = 1
            else:
                pass
        elif original[i][(j+1)%size] == 1:
            if random.random() <= prob1:  # checking probability 1
                original[i][j] = 1
            else:
                pass
        else:
            pass
        
    # if update point is infected take recovery action
    elif x == 1:
        if random.random() <= prob2:
            original[i][j] = 2
        else:
            pass
    # if update point is recovered form infection take susceptible action
    elif x == 2:
        if random.random() <= prob3:
            original[i][j] = 0
        else:
            pass
    return original  # return the updated array

def dat_wrtiter_1(Im,avgI):
    f = open('immuneplot.dat', 'a')
    f.write('%f %f \n' %(Im, avgI))
    f.close()

# for Immunity problem
def main():
    for Im in tqdm(np.arange(0, 1, 0.01)):
        size = 50  # size fixed as 50.
        prob1 = 0.5  # prob1 fixed as 0.5.
        prob2 = 0.5  # prob2 fixed as 0.5.
        prob3 = 0.5  # prob3 fixed as 0.5.
        lattice = initialize(size)  # initialized the lattice.
        lattice = Immun_generator(size, lattice, Im)
        nsteps = 1100  # number of steps given.
        TotalI = 0  # variable gets total number of I from IperSwp each sweep.

        for n in range(nsteps):
            # calling one sweep
            for i in range(size * size):
                lattice = SIR(size, lattice, prob1, prob2, prob3)  # p1 infection/ p2 recovery/ p3 susceptible again
            # wait for equilibration
            if n >= 100:
                if n % 10 == 0:
                    IperSwp = int(np.argwhere(lattice==1).shape[0]) # number of I on lattice per sweep.
                    TotalI += IperSwp  # add the IperSwp to Var. TotalI outside of loop.
        averageI = TotalI / 100  # average I is totalI divided by number of sweep (1000 sweeps)
        avg_rate_I = averageI / (size * size)
        dat_wrtiter_1(Im, avg_rate_I)  # write out the plotting values


if __name__ == "__main__":
    main()