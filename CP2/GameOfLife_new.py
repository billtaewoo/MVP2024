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
        self.nsteps = measurement * 100
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
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
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
        for i in range(self.nsteps):
            self.rule()
            im.set_array(self.lattice)
            plt.pause(0.0001)
        plt.show()

        
    def measure(self):
        time = 0
        previous = np.sum(self.lattice)
        counter = 0
        for i in range(self.nsteps):
            self.rule()
            current = np.sum(self.lattice)
            if current == previous:
                counter += 1
            if counter > 50:
                time = i - 50
                # reset lattice before next measure
                self.lattice = np.random.choice([0,1],size=(self.size, self.size))
                break
            previous = current
        return time
    
    def histogram(self):
        times = np.zeros(self.measurement)
        for i in tqdm(range(self.measurement)):
            time = self.measure()
            times[i] = time
        data = {"time":[]}
        for j in range(self.measurement):
            data["time"].append(times[j])
        # save dictionary data to a csv file using pandas
        df = pd.DataFrame(data)
        df.to_csv("histogram.csv",index=True)
        print(f"Data saved successfully!")

def main():
    x= GameofLife(50,"random",1000)
    # x.animate()
    x.histogram()
main()