import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import csv
import pandas as pd
from tqdm import tqdm

class SIRS:
    def __init__(self, size, measurements, prob1, prob2, prob3, prob_Im = 0, case="SIRS"):
        self.size = int(size)
        self.p1 = prob1
        self.p2 = prob2
        self.p3 = prob3
        # self.p_Im = prob_Im
        self.case = case
        self.measurements = int(measurements)
        self.nsteps = self.measurements * 10 + 100 # measurement * decorrelation time * equilibration time
        self.lattice = np.random.choice([0,1,2], size=(self.size,self.size))
        # if case == "SIRS":
        #     self.lattice = np.random.choice([0,1,2], size=(self.size,self.size))
        # elif case == "Immune":
        #     self.lattice = np.random.choice([0,1,2], size=(self.size,self.size))
        #     pop = int((self.size **2) * self.p_Im)
        #     x = np.random.randint(0, self.size, size = pop)
        #     y = np.random.randint(0, self.size, size = pop)
        #     self.lattice[y,x] = 3 #make it immune

    def updates(self):
        iteration = int(self.size ** 2)
        #get list of x,y random coordinate
        x = np.random.randint(0, self.size, size= iteration)
        y = np.random.randint(0, self.size, size= iteration)
        for i in range(iteration):
            X = x[i]
            Y = y[i]
            up = self.lattice[(Y+1)%self.size,X]
            down = self.lattice[(Y-1)%self.size,X]
            right = self.lattice[Y,(X+1)%self.size]
            left = self.lattice[Y,(X-1)%self.size]
            if self.lattice[Y,X] == 0 :
                if up == 1:
                    self.lattice[Y,X] = random.choices([1,0], weights=[self.p1,1-self.p1], k=1)[0]
                elif down == 1:
                    self.lattice[Y,X] = random.choices([1,0], weights=[self.p1,1-self.p1], k=1)[0]
                elif right == 1:
                    self.lattice[Y,X] = random.choices([1,0], weights=[self.p1,1-self.p1], k=1)[0]
                elif left == 1:
                    self.lattice[Y,X] = random.choices([1,0], weights=[self.p1,1-self.p1], k=1)[0]
            elif self.lattice[Y,X] == 1:
                self.lattice[Y,X] = random.choices([2,1], weights=[self.p2,1-self.p2], k=1)[0]
            elif self.lattice[Y,X] == 2:
                self.lattice[Y,X] = random.choices([0,2], weights=[self.p3,1-self.p3], k=1)[0]
    
    def immune(self):
        pop = int((self.size **2) * self.p_Im)
        x = np.random.randint(0, self.size, size = pop)
        y = np.random.randint(0, self.size, size = pop)
        self.lattice[y,x] = 3 #make it immune

    
    def animate(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self.lattice)
        for i in range(self.nsteps):
            self.updates()
            im.set_array(self.lattice)
            plt.pause(0.0001)
        plt.show()

    def cal_Inum(self):
        I_num = np.count_nonzero(np.lattice == 1)
        return I_num

    def bootstrap(self, lists, nsets= 1000):
        array = np.array(lists)
        setsize = len(array)
        rand_indices = np.random.randint(0, setsize, size = (setsize, nsets), dtype=int) # array of random coordinates
        sets = array[rand_indices]
        vars = np.var(sets, axis = 0)
        error = np.std(vars, axis= 0)
        return error

def main():
    x = SIRS(50,100,0.6,0.5,0.1)

    x.animate()

main()