import numpy as np
import matplotlib.pyplot as plt

class Ising:
    def __init__(self, size, init, temperature, measurements):
        self.size = int(size)  # get the size
        self.temp = temperature  # get the temperature of system
        # measurement is number of mesaurements 
        # 10 is decorrelation between next measurement
        # 100 is equilibration steps 
        self.nsteps = int(measurements * 10 + 100)
        self.measurements = measurements
        if init == "random":
            self.lattice = np.random.choice([-1, 1], size=(self.size,self.size))  # random lattice
        elif init == "homogeneous":
            self.lattice = np.ones((self.size,self.size), dtype=int)  # homogeneous lattice
        elif init == "half":
            self.lattice = np.zeros((self.size,self.size), dtype=int)
            self.lattice[:size//2, :] = 1
            self.lattice[size//2:, :] = -1
            #  half lattice
    
    def glauber_updater(self):
        Iteration = int(self.size ** 2)
        # generating list length of iteration of random x and y coordinates
        x = np.random.randint(0, self.size, size = Iteration)
        y = np.random.randint(0, self.size, size = Iteration)
        for i in range(Iteration):
            neighbour = (self.lattice[y[i]][(x[i]+1)%self.size] + 
                         self.lattice[y[i]][(x[i]-1)%self.size] + 
                         self.lattice[(y[i]+1)%self.size][x[i]] + 
                         self.lattice[(y[i]-1)%self.size][x[i]])
            eng = -1 * self.lattice[y[i]][x[i]] * neighbour
            eng_new = -1 * -1 * self.lattice[y[i]][x[i]] * neighbour
            eng_diff = eng_new - eng
            prob = min(1, np.exp(-1 * eng_diff / self.temp))
            self.lattice[y[i]][x[i]] = np.random.choice([self.lattice[y[i]][x[i]], -1* self.lattice[y[i]][x[i]]], 1, p=[1-prob, prob])

    def kawasaki_updater(self):
        Iteration = int((self.size ** 2)/2) # one sweep is no of iterations for picking entire lattice
        # kawaski halves Iteration because we are picking two points at once
        # generating list length of iteration of random x and y coordinates (2 coordinates this time)
        x1 = np.random.randint(0, self.size, size = Iteration)
        y1 = np.random.randint(0, self.size, size = Iteration)
        x2 = np.random.randint(0, self.size, size = Iteration)
        y2 = np.random.randint(0, self.size, size = Iteration)
        for i in range(Iteration):
            neighbours1 = (
            self.lattice[y1[i]][(x1[i] + 1) % self.size] +
            self.lattice[y1[i]][(x1[i] - 1) % self.size] +
            self.lattice[(y1[i] + 1) % self.size][x1[i]] +
            self.lattice[(y1[i] - 1) % self.size][x1[i]]
            )
            neighbours2 = (
            self.lattice[y2[i]][(x2[i] + 1) % self.size] +
            self.lattice[y2[i]][(x2[i] - 1) % self.size] +
            self.lattice[(y2[i] + 1) % self.size][x2[i]] +
            self.lattice[(y2[i] - 1) % self.size][x2[i]]
            )
            eng_1 = -1 * self.lattice[y1[i]][x1[i]] * neighbours1
            eng_2 = -1 * self.lattice[y2[i]][x2[i]] * neighbours2
            eng_old = eng_1 + eng_2 # original energy
            new_eng_1 = -1 * -1 * self.lattice[y1[i]][x1[i]] * neighbours1
            new_eng_2 = -1 * -1 * self.lattice[y2[i]][x2[i]] * neighbours2
            eng_new = new_eng_1 + new_eng_2 # new energy
            # condition if two random points are right next to each other
            if abs(y1[i]-y2[i]) == 1 or abs(x1[i] - x2[i]) == 1:
                eng_old -= self.lattice[y1[i]][x1[i]] * self.lattice[y2[i]][x2[i]]
                eng_new -= (-1 * self.lattice[y1[i]][x1[i]]) * (-1 * self.lattice[y2[i]][x2[i]])
            else: pass
            eng_diff = eng_new - eng_old
            prob = min(1, np.exp(-1 * eng_diff / self.temp))
            self.lattice[y1[i]][x1[i]] = np.random.choice([self.lattice[y1[i]][x1[i]], -1* self.lattice[y1[i]][x1[i]]], 1, p=[1-prob, prob])
            self.lattice[y2[i]][x2[i]] = np.random.choice([self.lattice[y2[i]][x2[i]], -1* self.lattice[y2[i]][x2[i]]], 1, p=[1-prob, prob])
    
    def eng_total(self):
        neighbours = (np.roll(self.lattice, 1, axis=0)+
                      np.roll(self.lattice,-1, axis=0)+
                      np.roll(self.lattice, 1, axis=1)+
                      np.roll(self.lattice,-1, axis=1))
        eng = -1 * self.lattice * neighbours
        eng_total = 0.5 * np.sum(eng)
        return eng_total
    
    def magnt_total(self):
        mgnt_total = np.sum(self.lattice)
        return mgnt_total
    
    def heat_cap(self, energy):
        avg_eng = np.mean(energy)
        avg_eng2 = np.mean(np.square(energy))
        dev = avg_eng2 - avg_eng**2
        heat_cap = (1/(self.size**2 * self.temp**2)) * dev
        return heat_cap
    
    def mag_sus(self, magnt):
        avg_mgnt = np.mean(magnt)
        avg_mgnt2 = np.mean(np.sqare(magnt))
        dev = avg_mgnt2 - avg_mgnt**2
        mag_sus = (1/(self.size**2 * self.temp)) * dev
        return mag_sus

    def bootstrap(self, array, nsets= 1000):
        setsize = len(array)
        rand_indices = np.random.randint(0, len(array), size = (setsize, nsets)) # array of random coordinates
        sets = array[rand_indices]
        vars = np.var(sets, axis = 0)
        error = np.std(vars, axis= 0)
        return error
    
    def hc_error(self, sample):
        hc = np.zeros(len(sample))
        for i in range(len(sample)):
            hc[i] = self.heat_cap(sample[i])
        error = np.std(hc)
        return error
    
    def ms_error(self, sample):
        ms = np.zeros(len(sample))
        for i in range(len(sample)):
            ms[i] = self.mag_sus(sample[i])
        error = np.std(ms)
        return error
    
    def glauber_animator(self):
        fig, ax = plt.subplots()  # generate the figure
        im = ax.imshow(self.lattice)
        for i in range(self.nsteps):
            self.glauber_updater()
            im.set_array(self.lattice)
            plt.pause(0.0001)
        plt.show()

    def kawasaki_animator(self):
        fig, ax = plt.subplots()  # generate the figure
        im = ax.imshow(self.lattice)
        for i in range(self.nsteps):
            self.kawasaki_updater()
            im.set_array(self.lattice)
            plt.pause(0.0001)
        plt.show()

    def glauber_measure(self):
        eng = []
        mgnt = []
        for i in range(self.nsteps):
            self.glauber_updater()
            if i >= 100:
                if i % 10 == 0:
                    eng.append(self.eng_total())
                    mgnt.append(self.magnt_total())
        hc = self.heat_cap(eng)
        sus = self.mag_sus(mgnt)
                    




def main():
    x = Ising(50,"random",2,100)
    # x.glauber_animator()
    # x.kawasaki_animator()

main()

