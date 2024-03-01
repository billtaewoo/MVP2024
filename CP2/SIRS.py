import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import random
from tqdm import tqdm
from matplotlib import pyplot as plt
import csv

'''
    S : susceptible to the infection (0)
    I : infected                     (1)   
    R : recovered from the infection (2)
'''

def initialize(size):
    # part for generate the random array of given size
    return np.random.choice([0, 1, 2], size=(size, size))

def SIR(size, array, prob1, prob2, prob3):

    original = array  # copy original
    #copy = original  # empty copy get update

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

def csv_wrtiter(p1,p3,avgI):
    with open('p1p3plot.csv', mode='a') as plot_file:
        plot_writer = csv.writer(plot_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        plot_writer.writerow([p1, p3, avgI])

'''
End of the functions.
'''


'''
def main():
    size, prob1, prob2, prob3 = map(float, input().split()) # taking variables
    size = int(size)
    lattice = initialize(size)  # initialized the lattice
    nsteps = 1000  # number of steps given

    for n in tqdm(range(nsteps)):
        # calling one sweep
        for i in range(size * size):
            lattice = SIR(size, lattice, prob1, prob2, prob3)  # p1 infection/ p2 recovery/ p3 susceptible again
        plt.cla()
        im = plt.imshow(lattice, animated=True)
        plt.draw()
        plt.pause(0.0001)
'''

def main():
    for prob1 in tqdm(np.arange(0, 1, 0.01)):  # increase prob1 by increment of 0.05.
        for prob3 in tqdm(np.arange(0, 1, 0.01)):  # increase prob3 by increment of 0.05.
            size = 50  # size fixed as 50.
            prob2 = 0.5  # prob2 fixed as 0.5.
            lattice = initialize(size)  # initialized the lattice.
            nsteps = 1100  # number of steps given.
            TotalI = 0  # variable gets total number of I from IperSwp each sweep.

            for n in tqdm(range(nsteps)):
                # calling one sweep
                for i in range(size * size):
                    lattice = SIR(size, lattice, prob1, prob2, prob3)  # p1 infection/ p2 recovery/ p3 susceptible again
                # wait for equilibration
                if n >= 100:
                    IperSwp = int(np.argwhere(lattice==1).shape[0]) # number of I on lattice per sweep.
                    TotalI += IperSwp  # add the IperSwp to Var. TotalI outside of loop.
            averageI = TotalI / (nsteps-100)  # average I is totalI divided by number of sweep (1000 sweeps)
            print(averageI)

            csv_wrtiter(prob1, prob3, averageI)  # write out the plotting values to p1p3plot.csv

if __name__ == "__main__":
    main()