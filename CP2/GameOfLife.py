import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import csv
import pandas as pd
from tqdm import tqdm

class GameofLife:
    def __init__(self, size, type, measurement):
        self.size = int(size)
        self.measurement = int(measurement)
        if type == "random":
            self.lattice = np.random.choice([0,1],size=(self.size, self.size))
        elif type == "oscillators":
            self.lattice = np.zeros((size,size))
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            if self.lattice[y,x] == 0:
                self.lattice[y,x] = 1
                self.lattice[y, (x-1)%self.size] = 1
                self.lattice[y, (x+1)%self.size] = 1
        elif type == "gliders":
            self.lattice = np.zeros((size,size))
            #x = np.random.randint(0, self.size)
            #y = np.random.randint(0, self.size)
            x = 0
            y = 0
            if self.lattice[y,x] == 0:
                self.lattice[(y-1)%self.size,x] = 1
                self.lattice[y,(x+1)%self.size] = 1
                self.lattice[(y+1)%self.size,(x+1)%self.size] = 1
                self.lattice[(y+1)%self.size,x] = 1
                self.lattice[(y+1)%self.size,(x-1)%self.size] = 1
    
    def rule(self):
        # Use convolution to generate lattice of neighbour sums
        filter = np.array([[1,1,1],[1,0,1],[1,1,1]])
        neighbour = scipy.ndimage.convolve(self.lattice, filter, mode='wrap')
        # use boolean index
        self.lattice[(self.lattice == 1) & (neighbour < 2)] = 0  # Rule 1
        self.lattice[(self.lattice == 1) & (neighbour == 2)] = 1  # Rule 2
        self.lattice[(self.lattice == 1) & (neighbour > 3)] = 0  # Rule 3
        self.lattice[(self.lattice == 0) & (neighbour == 3)] = 1  # Rule 4

    def animate(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self.lattice)
        for i in range(self.measurement):
            self.rule()
            im.set_array(self.lattice)
            plt.pause(0.0001)
        plt.show()

        
    def measure(self, maxnruns = 2000):
        previous = np.sum(self.lattice)
        counter = 0
        for i in range(maxnruns):
            self.rule()
            current = np.sum(self.lattice)
            if current == previous:
                counter += 1
            if counter > 50:
                
                # reset lattice before next measure
                self.lattice = np.random.choice([0,1],size=(self.size, self.size))
                return  i - 50
                
            previous = current
        # reset lattice before next measure
        self.lattice = np.random.choice([0,1],size=(self.size, self.size))
        return i
    
    def histogram(self, maxnruns = 2000):
        times = np.zeros(self.measurement)
        for i in tqdm(range(self.measurement)):
            time = self.measure(maxnruns=maxnruns)
            times[i] = time
        data = {"time":[]}
        for j in range(self.measurement):
            data["time"].append(times[j])
        # save dictionary data to a csv file using pandas
        df = pd.DataFrame(data)
        df.to_csv("histogram.csv",index=True)
        print(f"Data saved successfully!")
        plt.hist(times, bins = 50)
        plt.show()
    
    def Com(self):
        m_sums = np.sum(np.argwhere(self.lattice == 1), axis = 0)
        com = m_sums/np.sum(self.lattice)
        return com
        
    def Com_Calc(self, limit=51):
   
        data = {"time":[],"com_x":[],"com_y":[], "velocity":[]}
        for i in range(limit):
            self.rule()
            com = self.Com()
            if i > 1:
                data["com_x"].append(com[0])
                data["com_y"].append(com[1])
                data["time"].append(i)
                data["velocity"].append(np.sqrt(com[0]**2+com[1]**2)/i)

        df = pd.DataFrame(data)
        df.to_csv("Center_Mass.csv",index=True)
        print(f"Data saved successfully!")
        plt.scatter(data["com_x"], data["com_y"])
        plt.show()
        vel = np.mean(data["velocity"])
        print("velocity of the glider is " + str(vel))


def main():
    x= GameofLife(50,"random", 1000)
    x.animate()
    # x.histogram()
    # x.Com_Calc()
main()