import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread
import IsingModel as IM

class ising_animation(object):
    def __init__(self, model, iterations):
        self.model = model
        self.iterations = iterations
        self.fig, self.ax = plt.subplots()
        self.implot = self.ax.imshow(self.model.arr)  # take array from Ising model
        self.ani = None  # for storing the animation object
    def run(self):
        thread = Thread(target=self.model.run, args=(self.iterations,))
        # start simulation thread
        thread.start()
        # start the animation in the main thread
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=10, blit=True)
        plt.show()
        self.model.stop()
    def animate(self, frame):
        # update the image to show the latest orientation of array
        self.implot.set_data(self.model.arr)
        # return
        return [self.implot]

def main():
    size = 10
    temp = 1
    model_type = "glauber"
    model = IsingModel(size, temp, model_type)
    anim = ising_animation(model, iterations=100)
    anim.run()
main()