import numpy as np
import matplotlib.pyplot as plt
import numpy.random


class IsingModel(object):
    def __init__(self, size, temp):
        self.size = size  # set size
        self.arr = np.zeros(shape=(size, size))  # set up the empty array
        for i in range(size):  # fill the array with -1 or 1 spin values
            for j in range(size):
                if np.random.random() < 0.5:
                    self.arr[i][j] = -1
                else:
                    self.arr[i][j] = 1
        self.temp = temp  # set temperature
        self.indi = np.zeros(shape=(2, 2))  # generating initial coordinate indices

    def glauber_dyn(self):
        array = self.arr  # load the array generated initially
        # indi = np.zeros(2)   generating initial coordinate indices
        indi = self.indi
        indi[0][0] = int(np.random.random() * self.size)  # generate random y coordinate
        indi[0][1] = int(np.random.random() * self.size)  # generate random x coordinate
        mu_point = array[int(indi[0][0])][int(indi[0][1])]  # point out the random coordinate on array
        nu_point = 0  # empty variable for flipped spin point
        if mu_point < 0:  # attempt to update the spin on pointer
            nu_point = mu_point * -1  # flips the spin if spin is -1
        else:
            nu_point = mu_point * -1  # flips the spin if spin is +1

        if int(indi[0][1]) + 1 > self.size - 1:  # set up boundary condition for right neighbour
            pt_r = array[int(indi[0][0])][self.size % (int(indi[0][1]) + 1)]  # roll the overflowing pt and choose right spin
        else:
            pt_r = array[int(indi[0][0])][int(indi[0][1]) + 1]  # choose spin on right of point

        if int(indi[0][1]) - 1 < 0:
            pt_l = array[int(indi[0][0])][self.size + (int(indi[0][1]) - 1)]  # set up boundary condition for left neighbour
        else:
            pt_l = array[int(indi[0][0])][int(indi[0][1])-1]  # choose left

        if int(indi[0][0]) - 1 < 0:  # set up boundary condition for up neighbour
            pt_u = array[self.size + (int(indi[0][0])-1)][int(indi[0][1])]
        else:
            pt_u = array[int(indi[0][0]) - 1][int(indi[0][1])]  # up

        if int(indi[0][0]) + 1 > self.size - 1:  # set up boundary condition for down neighbour
            pt_d = array[self.size % (int(indi[0][0]) + 1)][int(indi[0][1])]
        else:
            pt_d = array[int(indi[0][0]) + 1][int(indi[0][1])]  # down

        sum_neighbour = int(pt_u + pt_d + pt_r + pt_l)  # sum of all energy of neighbour
        mu_E = int(mu_point) * sum_neighbour  # sum of energy of initial state (mu)
        nu_E = int(nu_point) * sum_neighbour  # sum of energy of flipped state (nu)
        self.DE = int(nu_E) - int(mu_E)  # difference of energy
        self.prob = min(1, np.exp(-self.DE/self.temp))  # Metropolis algorithm of probability



    def kawasaki_dyn(self):
        array = self.arr  # load the array generated initially
        indi = np.zeros(shape=(2, 2))  # generating initial coordinate indices
        for i in range(2):  # loop two times to find two random coordinates
            indi[i][0] = int(np.random.random() * self.size)  # generate random y coordinate of ith point
            indi[i][1] = int(np.random.random() * self.size)  # generate random x coordinate of ith point

        points = np.array([array[int(indi[0][0])][int(indi[0][1])], array[int(indi[1][0])][int(indi[1][1])]])
        # point out the spins on each random coordinate.
        pt_r = np.zeros(shape=(2, 1))
        pt_l = np.zeros(shape=(2, 1))
        pt_u = np.zeros(shape=(2, 1))
        pt_d = np.zeros(shape=(2, 1))  # make empty array of neighbour around two random points.
        for i in range(2):
            if int(indi[i][1]) + 1 > self.size - 1:  # set up boundary condition for right neighbour
                pt_r[i] = array[int(indi[i][0])][self.size % (int(indi[i][1]) + 1)]
            else:
                pt_r[i] = array[int(indi[i][0])][int(indi[i][1]) + 1]  # choose spin on right of point

            if int(indi[i][1]) - 1 < 0:
                pt_l[i] = array[int(indi[i][0])][self.size + (int(indi[i][1]) - 1)]
            else:
                pt_l[i] = array[int(indi[i][0])][int(indi[i][1])-1]  # choose left

            if int(indi[i][0]) - 1 < 0:  # set up boundary condition for up neighbour
                pt_u[i] = array[self.size + (int(indi[i][0])-1)][int(indi[i][1])]
            else:
                pt_u[i] = array[int(indi[i][0]) - 1][int(indi[i][1])]  # up

            if int(indi[i][0]) + 1 > self.size - 1:  # set up boundary condition for down neighbour
                pt_d[i] = array[self.size % (int(indi[i][0]) + 1)][int(indi[i][1])]
            else:
                pt_d[i] = array[int(indi[i][0]) + 1][int(indi[i][1])]  # down




    def stop(self):
        self.stopSim = True  # Stop!




def main():
    model = IsingModel()

