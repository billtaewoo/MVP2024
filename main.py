import os
import sys
import numpy as np

def main():
    size = 10
    arr = np.zeros(shape=(size, size))
    for i in range(size):
        for j in range(size):
            if np.random.random() < 0.5:
                arr[i][j] = -1
            else:
                arr[i][j] = 1

    array = arr  # load the array generated initially

    indi = np.zeros(shape=(2, 2))  # generating initial coordinate indices
    for i in range(2):  # loop two times to find two random coordinates
        indi[i][0] = int(np.random.random() * size)  # generate random y coordinate of ith point
        indi[i][1] = int(np.random.random() * size)  # generate random x coordinate of ith point

    mu_points = np.array([array[int(indi[0][0])][int(indi[0][1])], array[int(indi[1][0])][int(indi[1][1])]])
    # point out the random coordinate on array generated initially
    pt_r = np.zeros(shape=(2, 1))
    pt_l = np.zeros(shape=(2, 1))
    pt_u = np.zeros(shape=(2, 1))
    pt_d = np.zeros(shape=(2, 1))  # make empty array of neighbour around two random points.
    for i in range(2):
        if int(indi[i][1]) + 1 > size - 1:  # set up boundary condition for right neighbour
            pt_r[i] = array[int(indi[i][0])][size % (int(indi[i][1]) + 1)]
        else:
            pt_r[i] = array[int(indi[i][0])][int(indi[i][1]) + 1]  # choose spin on right of point

        if int(indi[i][1]) - 1 < 0:
            pt_l[i] = array[int(indi[i][0])][size + (int(indi[i][1]) - 1)]
        else:
            pt_l[i] = array[int(indi[i][0])][int(indi[i][1]) - 1]  # choose left

        if int(indi[i][0]) - 1 < 0:  # set up boundary condition for up neighbour
            pt_u[i] = array[size + (int(indi[i][0]) - 1)][int(indi[i][1])]
        else:
            pt_u[i] = array[int(indi[i][0]) - 1][int(indi[i][1])]  # up

        if int(indi[i][0]) + 1 > size - 1:  # set up boundary condition for down neighbour
            pt_d[i] = array[size % (int(indi[i][0]) + 1)][int(indi[i][1])]
        else:
            pt_d[i] = array[int(indi[i][0]) + 1][int(indi[i][1])]  # down

    return array, indi, mu_points, pt_u, pt_l, pt_r, pt_d

arr, indi, mu, u, l, r, d = main()

print(arr, indi, mu, u, l, r, d)