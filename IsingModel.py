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
        pt = np.zeros(shape=(2, 2))  # generating empty initial coordinate indices
        self.pt_r = np.zeros(shape=(2, 1))
        self.pt_l = np.zeros(shape=(2, 1))
        self.pt_u = np.zeros(shape=(2, 1))
        self.pt_d = np.zeros(shape=(2, 1))  # make empty array of neighbour around two random points.
        for i in range(2):  # loop two times to find two random coordinates
            pt[i][0] = int(np.random.random() * self.size)  # generate random y coordinate of ith point
            pt[i][1] = int(np.random.random() * self.size)  # generate random x coordinate of ith point
        self.indi = pt  # generating initial coordinate indices
        for i in range(2):
            if int(self.indi[i][1]) + 1 > self.size - 1:  # set up boundary condition for right neighbour
                self.pt_r[i] = self.arr[int(self.indi[i][0])][self.size % (int(self.indi[i][1]) + 1)]
            else:
                self.pt_r[i] = self.arr[int(self.indi[i][0])][int(self.indi[i][1]) + 1]  # choose spin on right of point

            if int(self.indi[i][1]) - 1 < 0:
                self.pt_l[i] = self.arr[int(self.indi[i][0])][self.size + (int(self.indi[i][1]) - 1)]
            else:
                self.pt_l[i] = self.arr[int(self.indi[i][0])][int(self.indi[i][1])-1]  # choose left

            if int(self.indi[i][0]) - 1 < 0:  # set up boundary condition for up neighbour
                self.pt_u[i] = self.arr[self.size + (int(self.indi[i][0])-1)][int(self.indi[i][1])]
            else:
                self.pt_u[i] = self.arr[int(self.indi[i][0]) - 1][int(self.indi[i][1])]  # up

            if int(self.indi[i][0]) + 1 > self.size - 1:  # set up boundary condition for down neighbour
                self.pt_d[i] = self.arr[self.size % (int(self.indi[i][0]) + 1)][int(self.indi[i][1])]
            else:
                self.pt_d[i] = self.arr[int(self.indi[i][0]) + 1][int(self.indi[i][1])]  # down
        self.DE = np.zeros(shape=(2, 1))  # initialize empty array of Energy difference
        self.prob = np.zeros(shape=(2, 1))  # initialize empty array of probability

    def glauber_dyn(self, kawa):
        array = self.arr  # load the array generated initially
        indi = self.indi  # load the random coordinates generated initially
        r, l, u, d = self.pt_r, self.pt_l, self.pt_u, self.pt_d  # load neighbour coordinates of each random coords.
        if kawa == 1:
            for i in range(2):
                mu_pt = array[indi[i][0]][indi[i][1]]  # take value out i th random coordinate on array
                nu_pt = 0  # empty variable for flipped spin point
                if mu_pt < 0:  # attempt to update the spin of i th coordinate.
                    nu_pt = mu_pt * -1  # flips the spin if spin is -1
                else:
                    nu_pt = mu_pt * -1  # flips the spin if spin is +1
                sum_neighbour = int(r[i]+l[i]+u[i]+d[i])  # sum of all neighbour spins
                mu_E = int(mu_pt) * sum_neighbour  # sum of energy of mu states
                nu_E = int(nu_pt) * sum_neighbour  # sum of energy of nu states
                self.DE[i] = mu_E - nu_E  # difference of energy
                self.prob[i] = min(1, np.exp(-int(self.DE[i])/self.temp))  # Metropolis algorithm of probability
        else:
            i = 0
            mu_pt = array[indi[i][0]][indi[i][1]]  # take value out i th random coordinate on array
            nu_pt = 0  # empty variable for flipped spin point
            if mu_pt < 0:  # attempt to update the spin of i th coordinate.
                nu_pt = mu_pt * -1  # flips the spin if spin is -1
            else:
                nu_pt = mu_pt * -1  # flips the spin if spin is +1
            sum_neighbour = int(r[i] + l[i] + u[i] + d[i])  # sum of all neighbour spins
            mu_E = int(mu_pt) * sum_neighbour  # sum of energy of mu states
            nu_E = int(nu_pt) * sum_neighbour  # sum of energy of nu states
            self.DE_Glaub = int(nu_E) - int(mu_E)  # difference of energy
            self.prob_Glaub = min(1, np.exp(-int(self.DE_Glaub)/self.temp))  # Metropolis algorithm of probability

    def kawasaki_dyn(self):
        array = self.arr  # load the array generated initially
        indi = self.indi
        two_pts = np.array([array[int(indi[0][0])][int(indi[0][1])], array[int(indi[1][0])][int(indi[1][1])]])
        # point out the values of two spins on each random coordinate.
        self.glauber_dyn(1)  # call method 'glauber_dyn' and set parameter kawa==1 because it is used in kawasaki
        de_i = int(self.DE[0])  # DE of point i
        de_j = int(self.DE[1])  # DE of point j
        de_corr = int(two_pts[0]) * int(two_pts[1])  # correction DE of when i and j is the nearest neighbour.
        self.DE_kawa = de_i + de_j + de_corr  # sum of all DEs.
        self.prob_kawa = min(1, np.exp(-int(self.DE_kawa)/self.temp))  # Metropolis algorithm of probability







    def stop(self):
        self.stopSim = True  # Stop!




def main():
    model = IsingModel(10,1)

