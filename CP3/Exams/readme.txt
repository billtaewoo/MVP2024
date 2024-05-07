Hello Welcome to my exam code.
This file is for explaining how to run the code in other environment, and explaining methods.

1. Prerequisites
    In order to run the python code, you need to have following libraries:
        1. Numpy
        2. random (random comes with python)
        3. matplotlib.pyplot
        4. scipy.ndimage
        5. pandas
        6. tqdm (Nice littile library for printing out progress bar)

2. Code Structure
    This code is constructed as Object Oriented and it has a one class :Exam.

    class Exam is consists of following methods:
        1. __init__
            when class is called, it is requre two variables: size, type
            size is size of the lattice generating
            type is type of generator, which is differentiating by string given:
                if "fixed random" is given, it will generate lattice of given size where living cell with 0.01 probability.
                if "square" is given, it will generage the lattice with living cells shape square of size 20x20 in the middle.
                if "random" is given, it will generate totally random on and off lattice of given size. This condition of initialization is used for random sequential cellular automaton.
        
        2. rule
            This method is for update rule of deterministic cellular automation. This will update the whole lattice by following rules:
            Rule 1: if lattice is on, turn off
            Rule 2: if lattice is off and neighbour has exactly 2 (or 3, you can choose by delete the comment) on in 8 neighbours turn on
            This method utilizes convolution from scipy, so it is very fast.

        3. rule 2
            This method is for updating random sequential cellular automation.
            This method receives the p1 and p2 and updates by size * size amount, for a single sweep.
            random is used instead of np.random in order to reduce the time of the computation.

        4. animate
            This method is used for animating the deterministic cellular automation.
            maximum number of frame is defaulted to be 1000 (maxnruns)
        
        5. measure
            This metod is used for measuring the total living cell against time for the deterministic cellular automation.
            maximum number of frame is defaulted to be 2000 (maxnruns)
            data of plot is saved out via pandas as csv.

        6. heatmap
            This method is used for generating heatmap of the random sequential cellular automation.
            nsteps is defaulted to be 1100 (steps)
            It consists the for loop of picking the each p1 and p2 value for generating average fraction of time, and save scv via pandas.
            It supposed to show the plot of heat map via plt but it is now working (or doesn't have enough time to check it is working.). Yet the csv file exists.

        7. Variance_Calc
            This method was meant to be used for variance calculation, but unfortunatelly I was out of time.

3. Data files
    1. Time_VS_total_on_cells_plot.png 
        This is image of the plot from question b.
    2. timeVsLivingCellofN2.csv 
        This is csv data of the plot above.
    3. GoLHeatMap.csv
        This is csv data of the heatmap.