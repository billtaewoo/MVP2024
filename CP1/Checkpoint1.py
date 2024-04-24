import numpy as np
import random
import matplotlib.pyplot as plt
import csv
import pandas as pd
from tqdm import tqdm

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
            X = x[i]
            Y = y[i]
            neighbour = (self.lattice[Y,(X+1)%self.size] + 
                         self.lattice[Y,(X-1)%self.size] + 
                         self.lattice[(Y+1)%self.size,X] + 
                         self.lattice[(Y-1)%self.size,X])
            eng = -1 * self.lattice[Y,X] * neighbour
            eng_new = self.lattice[Y,X] * neighbour
            eng_diff = eng_new - eng
            prob = min(1, np.exp(-1 * eng_diff / self.temp))
            self.lattice[Y,X] = random.choices([self.lattice[Y,X], -1* self.lattice[Y,X]], weights=[1-prob, prob], k = 1)[0]

    def kawasaki_updater(self):
        Iteration = int((self.size ** 2)/2) # one sweep is no of iterations for picking entire lattice
        # kawaski halves Iteration because we are picking two points at once
        # generating list length of iteration of random x and y coordinates (2 coordinates this time)
        x1 = np.random.randint(0, self.size, size = Iteration)
        y1 = np.random.randint(0, self.size, size = Iteration)
        x2 = np.random.randint(0, self.size, size = Iteration)
        y2 = np.random.randint(0, self.size, size = Iteration)
        for i in range(Iteration):
            X1=x1[i]
            X2=x2[i]
            Y1=y1[i]
            Y2=y2[i]
            neighbours1 = (
            self.lattice[Y1,(X1 + 1) % self.size] +
            self.lattice[Y1,(X1 - 1) % self.size] +
            self.lattice[(Y1 + 1) % self.size,X1] +
            self.lattice[(Y1 - 1) % self.size,X1]
            )
            neighbours2 = (
            self.lattice[Y2,(X2 + 1) % self.size] +
            self.lattice[Y2,(X2 - 1) % self.size] +
            self.lattice[(Y2 + 1) % self.size,X2] +
            self.lattice[(Y2 - 1) % self.size,X2]
            )
            eng_1 = -1 * self.lattice[Y1,X1] * neighbours1
            eng_2 = -1 * self.lattice[Y2,X2] * neighbours2
            eng_old = eng_1 + eng_2 # original energy
            new_eng_1 = self.lattice[Y1,X1] * neighbours1
            new_eng_2 = self.lattice[Y2,X2] * neighbours2
            eng_new = new_eng_1 + new_eng_2 # new energy
            # condition if two random points are right next to each other
            if abs(Y1-Y2) == 1 or abs(X1 - X2) == 1:
                eng_old -= self.lattice[Y1,X1] * self.lattice[Y2,X2]
                eng_new -= (-1 * self.lattice[Y1,X1]) * (-1 * self.lattice[Y2,X2])
            else: pass
            eng_diff = eng_new - eng_old
            prob = min(1, np.exp(-1 * eng_diff / self.temp))
            self.lattice[Y1][X1] = random.choices([self.lattice[Y1][X1], -1* self.lattice[Y1][X1]], weights=[1-prob, prob], k=1)[0]
            self.lattice[Y2][X2] = random.choices([self.lattice[Y2][X2], -1* self.lattice[Y2][X2]], weights=[1-prob, prob], k=1)[0]
    
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
        return abs(mgnt_total)
    
    def heat_cap(self, energy):
        dev = np.var(energy)
        heat_cap = (1/(self.size**2 * self.temp**2)) * dev
        return heat_cap
    
    def mag_sus(self, magnt):
        dev = np.var(magnt)
        mag_sus = (1/(self.size**2 * self.temp)) * dev
        return mag_sus

    def bootstrap(self, lists, nsets= 1000):
        array = np.array(lists)
        setsize = len(array)
        rand_indices = np.random.randint(0, setsize, size = (setsize, nsets), dtype=int) # array of random coordinates
        sets = array[rand_indices]
        vars = np.var(sets, axis = 0)
        error = np.std(vars, axis= 0)
        return error
    
    def hc_error(self, error):
        return error / (self.size**2 * self.temp**2)
    
    def sus_error(self, error):
        return error / (self.size**2 * self.temp)
    
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
        hc = self.heat_cap(eng) # heat capacity
        sus = self.mag_sus(mgnt) # magnetic susceptibilty
        stdE = self.bootstrap(eng)  # standard deviation of Energy
        stdM = self.bootstrap(mgnt) # standard deviation of magnetisation
        hc_err = self.hc_error(stdE) # error of heat capacity
        sus_err = self.sus_error(stdM) # error of magnetic susceptibility
        avg_E = np.mean(eng)
        avg_M = np.mean(mgnt)
        return avg_E, avg_M, hc, sus, hc_err, sus_err
    
    def kawasaki_measure(self):
        eng = []
        mgnt = []
        for i in range(self.nsteps):
            self.glauber_updater()
            if i >= 100:
                if i % 10 == 0:
                    eng.append(self.eng_total())
                    mgnt.append(self.magnt_total())
        hc = self.heat_cap(eng) # heat capacity
        sus = self.mag_sus(mgnt) # magnetic susceptibilty
        stdE = self.bootstrap(eng)  # standard deviation of Energy
        stdM = self.bootstrap(mgnt) # standard deviation of magnetisation
        hc_err = self.hc_error(stdE) # error of heat capacity
        sus_err = self.sus_error(stdM) # error of magnetic susceptibility
        avg_E = np.mean(eng)
        avg_M = np.mean(mgnt)
        return avg_E, avg_M, hc, sus, hc_err, sus_err
    
    def glauber_generating(self, T_min=1, T_max=3, nsteps=20):
        # array for datas
        T = np.linspace(T_min,T_max,nsteps)
        E = np.zeros(nsteps)
        M = np.zeros(nsteps)
        hc = np.zeros(nsteps)
        sus = np.zeros(nsteps)
        hc_err = np.zeros(nsteps)
        sus_err = np.zeros(nsteps)
        data = {"T":[],"E":[],"M":[],"Hc":[],"Hc_err":[],"Msus":[],"Msus_err":[]} # dictionary value for save
        for i in tqdm(range(nsteps)):
            self.temp = T[i]
            E[i], M[i], hc[i], sus[i], hc_err[i], sus_err[i] = self.glauber_measure()
        # save to dictionary
        for j in range(nsteps):
            data["T"].append(T[j])
            data["E"].append(E[j])
            data["M"].append(M[j])
            data["Hc"].append(hc[j])
            data["Hc_err"].append(hc_err[j])
            data["Msus"].append(sus[j])
            data["Msus_err"].append(sus_err[j])
        # Save dictionary data to a CSV file using pandas
        df = pd.DataFrame(data)
        df.to_csv("glauber.csv", index=True)
        print(f"Data saved successfully!")

    def kawasaki_generating(self, T_min=1, T_max=3, nsteps=20):
        # array for datas
        T = np.linspace(T_min,T_max,nsteps)
        E = np.zeros(nsteps)
        M = np.zeros(nsteps)
        hc = np.zeros(nsteps)
        sus = np.zeros(nsteps)
        hc_err = np.zeros(nsteps)
        sus_err = np.zeros(nsteps)
        data = {"T":[],"E":[],"M":[],"Hc":[],"Hc_err":[],"Msus":[],"Msus_err":[]} # dictionary value for save
        for i in tqdm(range(nsteps)):
            self.temp = T[i]
            E[i], M[i], hc[i], sus[i], hc_err[i], sus_err[i] = self.kawasaki_measure()
        # save to dictionary
        for j in range(nsteps):
            data["T"].append(T[j])
            data["E"].append(E[j])
            data["M"].append(M[j])
            data["Hc"].append(hc[j])
            data["Hc_err"].append(hc_err[j])
            data["Msus"].append(sus[j])
            data["Msus_err"].append(sus_err[j])
        # Save dictionary data to a CSV file using pandas
        df = pd.DataFrame(data)
        df.to_csv("kawasaki.csv", index=True)
        print(f"Data saved successfully!")

def main():
    x = Ising(50,"half",2.5,100)
    # x.glauber_animator()
    x.kawasaki_animator()
    # x.glauber_generating()
    # x.kawasaki_generating()

main()

