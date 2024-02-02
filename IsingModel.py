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

    def apply_boundary_condition(self, coord):
        return coord % self.size

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
    def run(self, iterations):
        self.stopSim = False
        for i in range(iterations):
            if self.stopSim:
                break
            else:
                if self.model == "glauber":
                    self.glauber()
                elif self.model == "kawasaki":
                    self.kawasaki()
                else:
                    break


    def start_sim(self, model):
        if model == "glauber":
            self.glauber()
        elif model == "kawasaki":  # Corrected typo from "kawaski" to "kawasaki"
            self.kawasaki()
        else:
            print("type 'glauber' or 'kawasaki'")

    def stop(self):
        self.stopSim = True  # Stop!

class ising_animation(object):
    def __init__(self, model, iterations):
        self.model = model
        self.iterations = iterations
        self.fig, self.ax = plt.subplots()
        self.implot = self.ax.imshow(self.model.arr)  # take array from Ising model
        self.ani = None  # for storing the animation object
    def run(self):
        thread = Thread(target=self.model.run, args=(self.iterations,))
        # start simulation thread
        thread.start()
        # start the animation in the main thread
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=10, blit=True)
        plt.show()
        self.model.stop()
    def animate(self, frame):
        # update the image to show the latest orientation of array
        self.implot.set_data(self.model.arr)
        # return
        return [self.implot]







def main():
    size = 10
    temp = 1
    model_type = "glauber"
    model = IsingModel(size, temp, model_type)
    anim = ising_animation(model, iterations=100)
    anim.run()
main()


