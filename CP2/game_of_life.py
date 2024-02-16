import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from matplotlib import pyplot as plt


def generate_array(size):
    return np.random.choice([0, 1], size=(size, size))

def oscillators(size):
    array = np.zeros((size,size))
    x = np.random.randint(size)
    y = np.random.randint(size)
    if array[y][x] == 0:
        array[y][x] = 1
        array[y][(x-1)%size] = 1
        array[y][(x+1)%size] = 1
        return array

def moving_pattern(size):
    array = np.zeros((size,size))
    x = np.random.randint(size)
    y = np.random.randint(size)
    if array[y][x] == 0:
        array[(y-1)%size][x] = 1
        array[y][(x+1)%size] = 1
        array[(y+1)%size][(x+1)%size] = 1
        array[(y+1)%size][x] = 1
        array[(y+1)%size][(x-1)%size] = 1
        return array

def rule(array, size):
    n_arr = np.zeros((size,size))
    for y in range(size):
        for x in range(size):
            num = int(array[(y - 1) % size][x]
                + array[(y - 1) % size][(x + 1) % size]
                + array[y][(x + 1) % size]
                + array[(y + 1) % size][(x + 1) % size]
                + array[(y + 1) % size][x]
                + array[(y + 1) % size][(x - 1) % size]
                + array[y][(x - 1) % size]
                + array[(y - 1) % size][(x - 1) % size])
            if num < 2:  # rule 1
                if array[y][x] == 1:
                    n_arr[y][x] = 0
            elif num == 2:  # rule 2
                if array[y][x] == 1:
                    n_arr[y][x] = 1
            elif num > 3:  # rule 3
                if array[y][x] == 1:
                    n_arr[y][x] = 0
            elif num == 3:  # rule 4
                if array[y][x] == 1:
                    n_arr[y][x] = 1
                elif array[y][x] == 0:
                    n_arr[y][x] = 1
    return n_arr
def main():
    print("random or blinker or glider")
    ini = input()
    print("size")
    size = int(input())
    print("the number of steps")
    nsteps = int(input())
    if ini == 'random':
        array = generate_array(size)
    elif ini == 'blinker':
        array = oscillators(size)
    elif ini == 'glider':
        array = moving_pattern(size)


    for i in range(nsteps):
        array = rule(array, size)
        print(array.mean())
        plt.cla()
        im = plt.imshow(array, animated=True)
        plt.draw()
        plt.pause(0.0001)


if __name__ == "__main__":
    main()




