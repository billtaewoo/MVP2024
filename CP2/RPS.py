import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.ndimage
import csv
import pandas as pd
from tqdm import tqdm

class RPS:
    def __init__(self, size, measurement):
        self.size = size
        self.measurement = measurement
        self.lattice = self.set_wedges()

    def set_wedges(self):
        lattice = np.zeros((self.size, self.size), dtype=int)

        # Define the center of the lattice
        center_x = self.size // 2
        center_y = self.size // 2

        # Define the radius of the circle that inscribes the lattice
        radius = min(center_x, center_y)

        # Generate the grid of coordinates
        x, y = np.meshgrid(np.arange(self.size), np.arange(self.size))

        # Calculate the angle of each point with respect to the center
        angle = np.arctan2(y - center_y, x - center_x)

        # Create the first wedge (Rock)
        lattice[(angle >= -2*np.pi/3) & (angle <= 0)] = 1

        # Create the second wedge (Paper)
        lattice[(angle >= 0) & (angle <= 2*np.pi/3)] = 2

        # Create the third wedge (Scissors)
        lattice[(angle <= -2*np.pi/3) | (angle >= 2*np.pi/3)] = 3

        return lattice

    def plot(self):
        plt.imshow(self.lattice, cmap='viridis', vmin=1, vmax=3)
        plt.colorbar(ticks=[1, 2, 3], label='State')
        plt.title('Rock-Paper-Scissors Lattice')
        plt.show()
def main():
    x = RPS(50, 1000)
    x.plot()

main()