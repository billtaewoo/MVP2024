import numpy as np
import matplotlib.pyplot as plt

'''function return initial array'''
def initialize_array(size, initialize_type = "random", final_state = None):
    if final_state is not None:
        return final_state
    else:
        if initialize_type == "random":
            return np.random.choice([-1, 1], size=(size, size))
        elif initialize_type == "homogeneous":
            return np.ones((size, size), dtype=int)
        elif initialize_type == "half":
            array = np.zeros((size,size), dtype=int)
            array[:size//2, :] = 1
            array[size//2:, :] = -1
            return array

        else:
            print("Invalid initialization type!!")

'''generate random coordinate indices'''
def random_coordinate(size):
    x = np.random.randint(size)
    y = np.random.randint(size)
    return x, y

'''glauber dynamics spits out a new array after test'''
def glauber_dynamics(array, size, temperature, y, x):
    J = 1
    state = int(array[y][x])  # point out one among arrays
    neighbours = (
            array[y][(x + 1) % size] +
            array[y][(x - 1) % size] +
            array[(y + 1) % size][x] +
            array[(y - 1) % size][x]
    )
    new_state = -1 * state
    original_energy = -1 * J * (state * neighbours)
    new_energy = -1 * J * (new_state * neighbours)
    energy_difference = new_energy - original_energy
    probability = min(1, np.exp(-1 * energy_difference / temperature))

    if probability == 1:
        array[y][x] = new_state
        return array
    else:
        if np.random.random() < probability:
            array[y][x] = new_state
            return array
        else:
            return array
'''kawasaki dynamics spits out new array after test'''
def kawasaki_dynamics(array, size, temperature, y1, y2, x1, x2):
    J = 1
    state1 = int(array[y1][x1])
    state2 = int(array[y2][x2])  # get two random points given
    neighbours1 = (
            array[y1][(x1 + 1) % size] +
            array[y1][(x1 - 1) % size] +
            array[(y1 + 1) % size][x1] +
            array[(y1 - 1) % size][x1]
    )
    neighbours2 = (
            array[y2][(x2 + 1) % size] +
            array[y2][(x2 - 1) % size] +
            array[(y2 + 1) % size][x2] +
            array[(y2 - 1) % size][x2]
    )
    original_energy = (-1 * J * state1 * neighbours1) + (-1 * J * state2 * neighbours2)
    new_energy = (-1 * J * (-state1) * neighbours1) + (-1 * J * (-state2) * neighbours2)

    # Consideration of condition two selected points are neighbour to each other
    if abs(y1 - y2) == 1 or abs(x1 - x2) == 1:
        original_energy -= (state1 * state2)
        new_energy -= ((-state1) * (-state2))
    else:
        pass
    energy_difference = new_energy - original_energy
    probability = min(1, np.exp(-1 * energy_difference / temperature))

    if probability == 1:
        array[y1][x1] = -state1
        array[y2][x2] = -state2
        return array
    else:
        if np.random.random() <= probability:
            array[y1][x1] = -state1
            array[y2][x2] = -state2
            return array
        else:
            return array
'''energy calculated at each states and return total energy and square energy'''
def each_state_energy(array, size):
    energy = 0
    J = 1
    for i in range(size):
        for j in range(size):
            state = int(array[i][j])
            neighbours = (
                        array[i][(j + 1) % size] +
                        array[i][(j - 1) % size] +
                        array[(i + 1) % size][j] +
                        array[(i - 1) % size][j]
                )
            energy += -1 * J * state * neighbours
    return energy/2, (energy**2)/2  # prevent to double counting

'''magnetization calculated at each states and return magnetization and square magnetization'''

def each_state_magnetization(array, size):
    magnetization = 0
    for i in range(size):
        for j in range(size):
            magnetization += int(array[i][j])
    return magnetization, magnetization**2

'''function which creates the file for gnuplot.'''

def data_generation(filename, temperatures, energies, heat_capacities, abs_magnetizations, susceptibilities):
    data = np.column_stack((temperatures, energies, heat_capacities, abs_magnetizations, susceptibilities))
    np.savetxt(filename + "_values.txt", data, delimiter='\t')

def data_generation2(filename, energy_error, heat_capacities_errors, abs_magnetizations_errors, susceptibilities_errors):
    data = np.column_stack((energy_error, heat_capacities_errors, abs_magnetizations_errors, susceptibilities_errors))
    np.savetxt(filename + "_values.txt", data, delimiter='\t')



'''function to return bootstrap error'''

def bootstrap(data, nsteps):
    bootstrap = np.zeros(nsteps)
    for i in range(nsteps):
        resampling = np.random.choice(data, size=len(data), replace=True)
        bootstrap[i] = np.mean(resampling)

    error = np.std(bootstrap)
    return error

def main():
    print("Is this for play animation? (y/n)")
    switch = input("")

    if switch == "y":
        print("size?")
        size = int(input())
        print("temperature?")
        temperature = float(input())
        print("name of model?")
        name = str(input())
        nsteps = 250000
        final_state = None

        array = initialize_array(size)  # get random array

        fig, ax = plt.subplots()  # generate the figure
        im = ax.imshow(array)
        for i in range(nsteps):
            if name == "glauber":
                x, y = random_coordinate(size)
                array = glauber_dynamics(array, size, temperature, y, x)
            elif name == "kawasaki":
                x1, y1 = random_coordinate(size)
                x2, y2 = random_coordinate(size)
                # condition to prevent get a two coordinate at same position.
                while x1 == x2 or y1 == y2:
                    x2, y2 = random_coordinate(size)
                array = kawasaki_dynamics(array, size, temperature, y1, y2, x1, x2)
            else:
                print("type glauber or kawasaki")
                break
            if i % 2500 == 0:
                im.set_array(array)
                plt.pause(0.0001)
        plt.show()

    elif switch == "n":
        print("This is mode for plotting critical temperature.")
        print("size?")
        size = int(input())
        print("name of model?")
        name = str(input())
        temperature = 1.0
        nsteps = 100000

        # Data storage!
        temperatures = []
        energies = []
        heat_capacities = []
        abs_magnetizations = []
        susceptibilities = []
        # Error storage!
        energy_errors =[]
        heat_capacities_errors = []
        abs_magnetizations_errors = []
        susceptibilities_errors = []
        final_state = None
        while temperature <= 3.0:

            energy = []
            energy2 = []
            magnetization = []
            magnetization2 = []
            if name == "glauber":
                array = initialize_array(size, initialize_type="homogeneous")
            elif name == "kawasaki":
                array = initialize_array(size, initialize_type="half")
                #array = initialize_array(size)
            else:
                print("neither glauber, nor kawasaki")
                break
            for i in range(nsteps):
                if name == "glauber":
                    x, y = random_coordinate(size)
                    array = glauber_dynamics(array, size, temperature, y, x)  # updated array
                elif name == "kawasaki":
                    x1, y1 = random_coordinate(size)
                    x2, y2 = random_coordinate(size)
                    while x1 == x2 or y1 == y2:
                        x2, y2 = random_coordinate(size)
                    array = kawasaki_dynamics(array, size, temperature, y1, y2, x1, x2)  # updated array

                # wait to equilibration (100 sweeps)
                if i >= 100:
                    # takes measurement every 10 sweeps
                    if i % 10 == 0:
                        # measurement starts
                        e1, e2 = each_state_energy(array, size)
                        m1, m2 = each_state_magnetization(array, size)
                        energy.append(e1)
                        energy2.append(e2)

                        magnetization.append(m1)
                        magnetization2.append(m2)
                else:
                    continue
            # average values
            average_energy = np.average(energy)
            average_energy2 = np.average(energy2)
            average_magnetization = np.average(magnetization)
            average_magnetization2 = np.average(magnetization2)
            # size of N
            N = size ** 2
            # calculating specific heat
            heat_capacity = (1 / (N * temperature**2)) * (average_energy2 - average_energy**2)
            # calculating susceptibility
            suscpetibility = (1 / (N * temperature)) * (average_magnetization2 - average_magnetization**2)
            # save values before move on
            temperatures.append(temperature)
            energies.append(average_energy)
            heat_capacities.append(heat_capacity)
            abs_magnetizations.append(abs(average_magnetization))
            susceptibilities.append(suscpetibility)


            final_state = array.copy()  # use the final array again in next temperature
            temperature += 0.1  # increase the temperature
        #  calculate the errors
            energy_error = bootstrap(energies, nsteps)
            heat_capacities_error = bootstrap(heat_capacities, nsteps)
            magnetization_error = bootstrap(abs_magnetizations, nsteps)
            suscpetibility_error = bootstrap(susceptibilities, nsteps)
            # save errors before move on
            energy_errors.append(energy_error)
            heat_capacities_errors.append(heat_capacities_error)
            abs_magnetizations_errors.append(magnetization_error)
            susceptibilities_errors.append(suscpetibility_error)

        data_generation(name, temperatures, energies, heat_capacities, abs_magnetizations, susceptibilities)
        data_generation2("error", energy_errors, heat_capacities_errors, abs_magnetizations_errors,
                         susceptibilities_errors
                        )

    else:
        print("Invalid input. Please type y or n.")
        pass






main()