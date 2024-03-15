import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import math
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

def dat_wrtiter_1(p1,p3,avgI):
    f = open('heatmap_out.dat', 'a')
    f.write('%f %f %f\n' %(p1, p3, avgI))
    f.close()

def dat_wrtiter_2(p1,var,err):
    f = open('variance_out.dat', 'a')
    f.write('%f %f %f\n' %(p1, var, err))
    f.close()

def bootstrap(data, nsteps = 10):
    mean = np.zeros(nsteps)
    for i in range(nsteps):
        sample = np.random.choice(data, size=len(data), replace=True)
        mean[i] = np.mean(sample)
    
    err = np.std(mean)
    return err

'''
End of the functions.
'''

# For Showing animation

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

# For Heat map plotting problem
'''
def main():
    for prob1 in tqdm(np.arange(0, 1.05, 0.05)):  # increase prob1 by increment of 0.05.
        for prob3 in np.arange(0, 1.05, 0.05):  # increase prob3 by increment of 0.05.
            size = 50  # size fixed as 50.
            prob2 = 0.5  # prob2 fixed as 0.5.
            lattice = initialize(size)  # initialized the lattice.
            nsteps = 1100  # number of steps given.
            TotalI = 0  # variable gets total number of I from IperSwp each 10 sweeps.

            for n in range(nsteps):
                # calling one sweep
                for i in range(size * size):
                    lattice = SIR(size, lattice, prob1, prob2, prob3)  # p1 infection/ p2 recovery/ p3 susceptible again
                # wait for equilibration
                if n >= 100:
                    if n % 10 == 0:  # count every ten sweeps
                        IperSwp = int(np.argwhere(lattice==1).shape[0]) # number of I on lattice per sweep.
                        TotalI += IperSwp  # add the IperSwp to Var. TotalI outside of loop.
            averageI = TotalI / 100  # average I is totalI divided by number of sweep (100 sweeps)
            avg_rate_I = averageI / (size * size)
            dat_wrtiter_1(prob1, prob3, avg_rate_I)  # write out the plotting values to p1p3plot.dat
            '''
'''
# for Variance Plotting problem
def main():
    Vars = np.zeros(shape = (30, 2))  # empty array : rows = var for each p1, cols = var for each Itr
    # mean_vars = []  # storage for mean variances
    # err_vars = []  # storage for error of variances
    for Itr in tqdm(range(2), desc="number of iteration"):  # repeated iteration for bootstrap variance
        for prob1 in tqdm(np.arange(0.2, 0.5, 0.01),desc="number of varianceS calculation"):  # increase prob1 by increment of 0.05.
            rows = 0  # for row indexing
            size = 50  # size fixed as 50.
            prob2 = 0.5  # prob2 fixed as 0.5.
            prob3 = 0.5  # prob3 fixed as 0.5.
            lattice = initialize(size)  # initialized the lattice.
            nsteps = 10100  # number of steps given.
            TotalI = 0  # variable gets total number of I from IperSwp each sweep.
            TotalI2 = 0  # variable gets total numbrt of I square.

            for n in tqdm(range(nsteps),desc="a varaince calculation"):
                # calling one sweep
                for i in range(size * size):
                    lattice = SIR(size, lattice, prob1, prob2, prob3)  # p1 infection/ p2 recovery/ p3 susceptible again
                # wait for equilibration
                if n >= 100:
                    if n % 10 == 0:
                        IperSwp = int(np.argwhere(lattice==1).shape[0]) # number of I on lattice per sweep.
                        TotalI += IperSwp  # add the IperSwp to Var. TotalI outside of loop.
                        TotalI2 += IperSwp ** 2  # add the square Iperswp to var.
            averageI2 = TotalI2 / 1000  # average I square 
            averageI = TotalI / 1000  # average I is totalI divided by number of sweep (1000 sweeps)
            variance = (averageI2 - (averageI ** 2))/ (size * size)  # variance of I

            Vars[rows][Itr] = variance # plug value of variance into Vars.
            rows += 1  # to the next row indexing
    #Measuremets of variance fpr 1000 Itrs are over.
    for x in tqdm(range(30), desc="plotting..."):
        data = Vars[x, :] # get rows from x index position
        mean = (np.mean(data))  # append the mean of variance
        error = bootstrap(data)  # use bootstrap method to calculate error
        p1_num = 0.2
        dat_wrtiter_2(p1_num, mean, error)  # write out the plotting values to
        p1_num += 0.01
'''

if __name__ == "__main__":
    main()