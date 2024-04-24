import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import csv
import pandas as pd
from tqdm import tqdm

class GameofLife:
    def __init__(self, size, type):
        self.size = int(size)
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
        filter = np.array[[1,1,1],[1,0,1],[1,1,1]]
        neighbour = scipy.ndimage.convolve(self.lattice, filter, mode='wrap')
        # use boolean slicing index
        rule_1 = neighbour < 2 #coordinate fits rule 1
        rule_2 = neighbour == 2
        rule_3 = neighbour > 3
        rule_4 = neighbour == 3
        if self.lattice[rule_1] == 1:
            self.lattice[rule_1] = 0
        if self.lattice[rule_2] == 1:
            self.lattice[rule_2] = 1
        if self.lattice[rule_3] == 1:
            self.lattice[rule_3] = 0
        if self.lattice[rule_4] == 1:
            self.lattice[rule_4] = 1
        elif self.lattice[rule_4] == 0:
            self.lattice[rule_4] = 1
    
    def CoM(self):
        