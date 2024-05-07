import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import pandas as pd
from tqdm import tqdm

class Exam: 
    def __init__(self, size, type):
        self.size = size

        if type == "fixed random":
            p_i = 0.01
            self.lattice = np.random.choice([0, 1],size=(self.size, self.size), p=[1-p_i,p_i])
        if type == "square":
            self.lattice = np.zeros((self.size, self.size))
            #pick the center coordinate of the lattice
            center_x = self.size // 2
            center_y = self.size // 2
            # generate the grid of coordinates
            x, y = np.meshgrid(np.arange(self.size), np.arange(self.size))
            # generate the distance info grid from meshgrid
            x_side = x - center_x
            y_side = y - center_y
            # use boolean index
            self.lattice[(x_side>=-10)&(x_side<=9)&(y_side>= -10)&(y_side< 9)] = 1
        if type == "random":
            self.lattice = np.random.choice([0,1],size=(self.size, self.size))
    def rule(self):
        # generate kernel to apply convolution
        filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
        # apply convolution to get neighbour of the each cell and follow boundary condtiion
        neighbour = scipy.ndimage.convolve(self.lattice, filter, mode='wrap')
        # use boolean index
        self.lattice[(self.lattice == 1)] = 0 # Rule 1
        self.lattice[(self.lattice == 0) & (neighbour == 2)] = 1 # Rule 2-1
        # self.lattice[(self.lattice == 0) & (neighbour == 3)] = 1 # Rule 2-2

    def rule_2(self,p1,p2):
        # number of random choice in one sweep
        Iteration = int(self.size **2)
        # list of random picking coordinates
        x = np.random.randint(0, self.size, size = Iteration)
        y = np.random.randint(0, self.size, size = Iteration)
        for i in range(Iteration):
            # picking ith coordinate of random list above
            X = x[i]
            Y = y[i]
            # sum of all neighbours
            neighbour = (self.lattice[Y,(X+1)%self.size] + 
                         self.lattice[Y,(X-1)%self.size] + 
                         self.lattice[(Y+1)%self.size,X] + 
                         self.lattice[(Y-1)%self.size,X] +
                         self.lattice[(Y+1)%self.size,(X-1)%self.size]+
                         self.lattice[(Y+1)%self.size,(X+1)%self.size]+
                         self.lattice[(Y-1)%self.size,(X-1)%self.size]+
                         self.lattice[(Y-1)%self.size,(X+1)%self.size])
            if self.lattice[Y,X] == 1:
                self.lattice[Y,X] = random.choices([1, 0], weights=[1-p1, p1], k = 1)[0]
            elif self.lattice[Y,X] == 0 & neighbour == 2:
                self.lattice[Y,X] = random.choices([1, 0], weights=[p2, 1-p2], k = 1)[0]

    def animate(self, maxnruns = 1000):
        fig, ax = plt.subplots()
        im = ax.imshow(self.lattice)
        for i in range(maxnruns):
            self.rule()
            im.set_array(self.lattice)
            plt.pause(0.001)
        plt.show()

    def measure(self, maxnruns = 2000):
        # dictionary data to save
        data = {"time":[], "Number of living cell":[]}
        for i in range(maxnruns):
            # update
            self.rule()
            # measure total number of living cells
            total_I = np.sum(self.lattice)
            data["time"].append(i)
            data["Number of living cell"].append(total_I)
        # save directory data to a csv file using Pandas
        df = pd.DataFrame(data)
        df.to_csv("timeVsLivingCellOfN2.csv", index=True)
        print(f"Data saved successfully!")
        plt.title("The number of total alive state against time")
        plt.xlabel("time / frame")
        plt.ylabel("I/ The total living cells")
        plt.scatter(data["time"],data["Number of living cell"])
        plt.show()

    def heatmap(self, nsteps=1100):
        res = 5 # define resolution of heatmap
        # generate the array data of p1, p2 in given resolution
        p1 = np.linspace(0.1,1,res)
        p2 = np.linspace(0.1,1,res)
        # Dictionary data to save
        data = {"p1":[],"p2":[],"average fraction":[]}
        # start running loop for each p1 and p2 values 
        for i in tqdm(range(res)):
            for j in tqdm(range(res)):
                # repeat the sweep nsteptimes
                total_I = 0
                for n in tqdm(range(nsteps)):
                    self.rule_2(p1[i],p2[j])
                    #wait for equilibration
                    if n >= 100:
                        #plot data at every decorrelation
                        if n % 10 == 0:
                            # add the each number of "on" to Total_I
                            total_I += np.sum(self.lattice)
                # storing value to data
                data["average fraction"].append(total_I/nsteps)
                data["p1"].append(p1[i])
                data["p2"].append(p2[j])
        # save dictionary data to a csv file using pandas
        df = pd.DataFrame(data)
        df.to_csv("GoLHeatMap.csv",index=True)
        print(f"Data saved successfully!")
        #reshape the heat map size
        reshape_size = (res,res)
        plt.imshow(np.array(data["average fraction"]).reshape(reshape_size))
        plt.show()

    # def Variance_Calc(self,nsteps=1100):
    #     res = 10
    #     p1 = np.linspace(0.1,1,res)
    #     p2 = np.linspace(0.1,1,res)
    #     for i in range(res):
    #         for j in range(res):
    #             self.rule_2(p1[i],p2[j])
            




        
def main():
    x = Exam(100,"fixed random")
    # x.animate()
    # x.measure()

    y = Exam(100,"random")
    # y.heatmap()

main()