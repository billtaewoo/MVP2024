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

    indi = np.zeros(2)
    indi[0] = int(np.random.random()*size)
    indi[1] = int(np.random.random()*size)
    point = array[int(indi[0])][int(indi[1])]
    print(point)

main()