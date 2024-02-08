import os
import numpy as np
import matplotlib.pyplot as plt

class Ising(object):
    def __init__(self, size, temperature):
        self.temperature = temperature
        self.size = size
        self.array = self.initialize_array()  # generate instance random array

    def initialize_array(self):
        arr = np.random.choice([-1, 1], size=(self.size, self.size))
        return arr

    def random_coordinate(self):
        x = int(np.random.random() * self.size)
        y = int(np.random.random() * self.size)
        return x, y

    def glauber(self, y, x):  # get int as value
        J = 1
        state = int(self.array[y][x])
        neighbours = (
                self.array[y][(x + 1) % self.size] +
                self.array[y][(x - 1) % self.size] +
                self.array[(y + 1) % self.size][x] +
                self.array[(y - 1) % self.size][x]
        )

        new_state = -1 * state
        original_energy = -1 * J * (state * neighbours)
        new_energy = -1 * J * (new_state * neighbours)

        energy_difference = new_energy - original_energy
        probability = min(1, np.exp(-1 * energy_difference/self.temperature))

        if probability == 1:
            self.array[y][x] = new_state
        else:
            if np.random.random() <= probability:
                self.array[y][x] = new_state
            else:
                pass

    def kawasaki(self, y1, y2, x1, x2):

        J = 1
        state1 = int(self.array[y1][x1])
        state2 = int(self.array[y2][x2])
        neighbours1 = (
                self.array[y1][(x1 + 1) % self.size] +
                self.array[y1][(x1 - 1) % self.size] +
                self.array[(y1 + 1) % self.size][x1] +
                self.array[(y1 - 1) % self.size][x1]
        )

        neighbours2 = (
                self.array[y2][(x2 + 1) % self.size] +
                self.array[y2][(x2 - 1) % self.size] +
                self.array[(y2 + 1) % self.size][x2] +
                self.array[(y2 - 1) % self.size][x2]
        )

        original_energy = (-1 * J * state1 * neighbours1) + (-1 * J * state2 * neighbours2)
        new_energy = (-1 * J * (-state1) * neighbours1) + (-1 * J * (-state2) * neighbours2)

        if abs(y1 - y2) == 1 or abs(x1 - x2) == 1:
            original_energy -= (state1 * state2)
            new_energy -= ((-state1) * (-state2))
        else:
            pass
        energy_difference = new_energy - original_energy
        probability = min(1, np.exp(-1 * energy_difference/self.temperature))

        if probability == 1:
            self.array[y1][x1], self.array[y2][x2] = -state1, -state2
        else:
            if np.random.random() <= probability:
                self.array[y1][x1], self.array[y2][x2] = -state1, -state2
            else:
                pass

    def each_state_energy(self):
        energy = 0
        for i in range(self.size):
            for j in range(self.size):
                J = 1
                state = int(self.array[i][j])
                neighbours = (
                        self.array[i][(j + 1) % self.size] +
                        self.array[i][(j - 1) % self.size] +
                        self.array[(i + 1) % self.size][j] +
                        self.array[(i - 1) % self.size][j]
                )
                energy += -1 * J * state * neighbours
        return energy, energy**2
    def each_state_magnetization(self):
        magnetization = 0
        for i in range(self.size):
            for j in range(self.size):
                magnetization += int(self.array[i][j])
        return magnetization, magnetization ** 2




def main():
    print("Is this for play animation? (y/n)")
    switch = input()

    if switch == "y":
        print("size?")
        size = int(input())
        print("temperature?")
        temperature = float(input())
        print("name of model?")
        name = input()
        nsteps = 100000
        model = Ising(size, temperature)

        fig, ax = plt.subplots()
        im = ax.imshow(model.array, animated=True)
        for i in range(nsteps):
            if name == "glauber":
                x, y = model.random_coordinate()  # generate random coordinate
                model.glauber(y, x)
            elif name == "kawasaki":
                x1, y1 = model.random_coordinate()
                x2, y2 = model.random_coordinate()

                while x1 == x2 or y1 == y2:
                    x2, y2 = model.random_coordinate()

                model.kawasaki(y1, y2, x1, x2)
            else:
                print("type glauber or kawasaki")
                break
            if i % 2500 == 0:
                im.set_array(model.array)
                plt.pause(0.0001)

        plt.show()
    elif switch == "n":
        print("this is mode for plotting critical temperature.")
        print("size?")
        size = int(input())
        print("name of model?")
        name = input()
        temperature = 1.0
        nsteps = 100

        model = Ising(size, temperature)

        while temperature <= 3.0:
            for i in range(nsteps):
                if name == "glauber":
                    energy = 0
                    energy_square = 0
                    magnetization = 0
                    magnetization_square = 0
                    x, y = model.random_coordinate()
                    model.glauber(y, x)
                    e1, e2 = model.each_state_energy()
                    energy += e1
                    energy_square += e2
                    m1, m2 = model.each_state_magnetization()
                    magnetization += m1
                    magnetization_square += m2
                if name == "kawasaki":
                    energy = 0
                    energy_square = 0
                    magnetization = 0
                    magnetization_square = 0
                    x1, y1 = model.random_coordinate()
                    x2, y2 = model.random_coordinate()

                    while x1 == x2 or y1 == y2:
                        x2, y2 = model.random_coordinate()

                    model.kawasaki(y1, y2, x1, x2)

                    e1, e2 = model.each_state_energy()
                    energy += e1
                    energy_square += e2

                if i % 25 == 0:
                    print(temperature)
                    average_energy = energy / nsteps

                    average_energy_square = energy_square / nsteps

                    average_abs_magnetization = abs(magnetization) / nsteps

                    average_magnetization = magnetization / nsteps

                    average_magnetization_square = magnetization_square / nsteps


                    specific_heat = (average_energy_square - (average_energy ** 2))/(size * temperature ** 2)

                    susceptibility = (average_magnetization_square - average_magnetization ** 2)/(size * temperature)

                    temperature += 0.1






    else:
        print("invalid input. Please type y or n.")

main()








