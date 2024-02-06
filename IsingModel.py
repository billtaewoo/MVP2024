import os
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread

class IsingModel(object):
    def __init__(self, size, temp, model):
        self.temp = temp  # set temperature
        self.size = size  # set size
        self.model = model  # input value model
        self.arr = self.initialize_array()  # initialize the random array
        self.stopSim = False  # stop signal for simulation
        pt = np.zeros(shape=(2, 2), dtype=int)  # generating empty initial coordinate indices
        while self.arr[pt[0][0]][pt[0][1]] != self.arr[pt[1][0]][pt[1][1]]:
            for i in range(2):
                pt[i][0] = int(np.random.random() * self.size)  # generate random y coordinate of ith point
                pt[i][1] = int(np.random.random() * self.size)  # generate random x coordinate of ith point
                # Apply periodic boundary conditions
                pt[i][0] = pt[i][0] % self.size
                pt[i][1] = pt[i][1] % self.size
        self.indi = pt  # generating initial coordinate indices
        '''set the neighbour points of two coordinates'''
        self.right = np.zeros(shape=(2, 1))
        self.left = np.zeros(shape=(2, 1))
        self.up = np.zeros(shape=(2, 1))
        self.down = np.zeros(shape=(2, 1))  # make empty array of neighbour around two random points.
        for i in range(2):
            right_coord = self.apply_boundary_condition(int(pt[i][1]) + 1)
            left_coord = self.apply_boundary_condition(int(pt[i][1]) - 1)
            up_coord = self.apply_boundary_condition(int(pt[i][0]) - 1)
            down_coord = self.apply_boundary_condition(int(pt[i][0]) + 1)

            self.right[i] = self.arr[int(pt[i][0])][right_coord]
            self.left[i] = self.arr[int(pt[i][0])][left_coord]
            self.up[i] = self.arr[up_coord][int(pt[i][1])]
            self.down[i] = self.arr[down_coord][int(pt[i][1])]
    '''coordinates of neighbours : left, right, up, down'''
    def initialize_array(self):
        arr = np.random.choice([-1, 1], size=(self.size, self.size))
        return arr
    '''This is for generating initial random array.'''
    def apply_boundary_condition(self, coord):
        return coord % self.size
    '''This is for boundary condition.'''
    def glauber(self):
        state_right = int(self.right[0][0])
        state_left = int(self.left[0][0])
        state_up = int(self.up[0][0])
        state_down = int(self.down[0][0])  # states of neighbours
        state_mu = int(self.arr[self.indi[0][0]][self.indi[0][1]])  # take value out i th random coordinate on array
        state_nu = 0  # empty variable for flipped spin point
        state_nu = state_mu * -1  # flip the point
        sum_neighbour = -1 * int(state_right + state_left + state_up + state_down)  # sum of all neighbour spins
        energy_mu = state_mu * sum_neighbour  # sum of energy of mu states
        energy_nu = state_nu * sum_neighbour  # sum of energy of nu states
        diff_g = int(energy_nu - energy_mu)  # difference of energy
        prob_g = min(1, np.exp(-diff_g/self.temp))  # Metropolis algorithm of probability
        if prob_g == 1:
            self.arr[self.indi[0][0]][self.indi[0][1]] = state_nu  # changed
        else:
            if np.random.random() <= prob_g:
                self.arr[self.indi[0][0]][self.indi[0][1]] = state_nu  # changed
            else:
                self.arr[self.indi[0][0]][self.indi[0][1]] = state_mu  # unchanged
    '''It is part of Glauber dynamics'''
    def kawasaki(self):
        pre_energy = np.zeros(shape=(2, 1))
        after_energy = np.zeros(shape=(2, 1))
        for i in range(2):
            state_n = int(self.arr[self.indi[i][0]][self.indi[i][1]])
            sum_neighbour = -1 * (int(self.right[i][0]) + int(self.left[i][0]) + int(self.up[i][0]) + int(self.down[i][0]))
            pre_energy[i] = sum_neighbour * state_n  # store pre energy of each points
        for i in range(2):
            state_n = int(self.arr[self.indi[i][0]][self.indi[i][1]])
            new_state_n = state_n * -1  # flips the spin if spin is -1
            sum_neighbour = -1 * (int(self.right[i][0]) + int(self.left[i][0]) + int(self.up[i][0]) + int(self.down[i][0]))
            after_energy[i] = sum_neighbour * new_state_n  # store energy after change
        indi_difference = np.subtract(self.indi[0], self.indi[1])  # subtraction of two indices array
        if np.abs(indi_difference[0]) == 1 or np.abs(indi_difference[1]) == 1:
            x = np.subtract(after_energy, pre_energy)
            diff_k = int(np.sum(x)) - 1  # take out the redundant energy
        else:
            x = np.subtract(after_energy, pre_energy)
            diff_k = int(np.sum(x))
        prob_k = min(1, np.exp(-diff_k/self.temp))  # Metropolis algorithm of probability
        if prob_k == 1:
            for i in range(2):
                self.arr[self.indi[i][0]][self.indi[i][1]] = -1 * int(self.arr[self.indi[i][0]][self.indi[i][1]])
        else:
            if np.random.random() <= prob_k:
                for i in range(2):
                    self.arr[self.indi[i][0]][self.indi[i][1]] = -1 * int(self.arr[self.indi[i][0]][self.indi[i][1]])
            else:
                for i in range(2):
                    self.arr[self.indi[i][0]][self.indi[i][1]] = int(self.arr[self.indi[i][0]][self.indi[i][1]])
    '''It is part of Kawasaki Dynamics.'''
    def run(self, iterations, printFreq):
        self.stopSim = False
        for i in range(iterations):
            if self.stopSim:
                break
            if self.model == "glauber":
                self.glauber()
            elif self.model == "kawasaki":
                self.kawasaki()
            else:
                break
            # Draw and output the lattice configuration every printFreq steps
            if i % printFreq == 0:
                print("Iteration {:d}".format(i))
                self.printout()

    '''run the simulation in given amount of zweeps.'''
    def printout(self):
        outfile = "output.txt"
        tmpfile = outfile + ".tmp"
        # write the array first to temporary file
        with open(tmpfile, "w") as writer:
            for i in range(self.size):
                for j in range(self.size):
                    writer.write("{:d} {:d} {:d}\n".format(i, j, self.arr[i][j]))
                    # Add a newline after each row
                    writer.write("\n")
        # rename the temporary file to the output file
        os.rename(tmpfile, outfile)
    '''take the array data after given zweeps.'''
    def total_magnetisation(self, states):
        return np.sum(states)
    '''This is part of total magnetisation calculations.'''
    def total_energy(self, states):
        arr = states  # get array
        J = -1
        sums = 0
        for i in range(self.size):
            for j in range(self.size):
                x = int(arr[i][j])
                right = arr[i][self.apply_boundary_condition(j+1)]
                left = arr[i][self.apply_boundary_condition(j-1)]
                up = arr[self.apply_boundary_condition(i-1)][j]
                down = arr[self.apply_boundary_condition(i+1)][j]
                neighbours = int(right+left+up+down)
                sums += J * (x * neighbours)
        return sums
    '''This is part of total energy calculations.'''
    def mean_square(self, value):
        total_no = self.size * self.size
        square_M = value**2
        mean_square_M = square_M/total_no
        return mean_square_M
    '''This is part of general mean square calculations.'''
    def square_mean(self, states):
        mean_M = np.mean(states)
        sqr_mean_M = mean_M ** 2
        return sqr_mean_M
    '''This is part of general square mean calculations.'''
    def calculate_susceptibility(self, mean_square_M, square_mean_M):
        mean_sqr = mean_square_M
        sqr_mean = square_mean_M
        N = self.size * self.size
        m = (mean_sqr - sqr_mean)
        susceptibility = m / (N * self.temp)
        return susceptibility
    '''This is part of susceptibility calculations.'''
    def scaled_heat_capacity(self, mean_square_E, square_mean_E):
        mean_sqr = mean_square_E
        sqr_mean = square_mean_E
        N = self.size * self.size
        e = (mean_sqr - sqr_mean)
        scaled_heat_capacity = e / (N * (self.temp ** 2))
        return scaled_heat_capacity
    '''This is part of scaled heat capacity calculations.'''
    def start_sim(self, model):
        if model == "glauber":
            self.glauber()
        elif model == "kawasaki":  # Corrected typo from "kawaski" to "kawasaki"
            self.kawasaki()
        else:
            print("type 'glauber' or 'kawasaki'")
    '''This is module for simulator selection.'''
    def stop(self):
        self.stopSim = True  # Stop!
    '''This is for stop the simulator.'''


def main():
    size = 10
    temp = 1
    model_type = "glauber"
    iterations = 100
    printFreq = 5
    model = IsingModel(size, temp, model_type)
    model.run(iterations, printFreq)
    time.sleep(1)

main()


