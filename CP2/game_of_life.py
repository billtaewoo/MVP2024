import matplotlib
matplotlib.use('TKAgg')

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


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
def center_mass(array):
    # set origin as (0,0)
    vector_sum = np.sum(np.argwhere(array), axis=0)
    vec_length = np.linalg.norm(vector_sum)
    numbers = np.argwhere(array)[:, 0].size
    return vec_length/numbers

def main():
# part for input
    print("random or blinker or glider")
    ini = input()
    print("size")
    size = int(input())
    print("the number of steps")
    nsteps = int(input())
    if ini == 'random':
        lattice = generate_array(size)
    elif ini == 'blinker':
        lattice = oscillators(size)
    elif ini == 'glider':
        lattice = moving_pattern(size)

# part for generate animation.
    for n in tqdm(range(nsteps)):
        if ini == 'random':
            lattice = rule(lattice, size)
        if ini == 'glider':
            com = center_mass(lattice)
            f = open('output.txt', 'a')
            f.write('%d %d\n' %(com, n))
            f.close()
            lattice = rule(lattice, size)




        plt.cla()
        im = plt.imshow(lattice, animated=True)
        plt.draw()
        plt.pause(0.0001)


if __name__ == "__main__":
    main()




