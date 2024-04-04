# Set the output file type and name
set terminal pngcairo enhanced font 'Verdana,12'
set output 'vector_plot.png'

# Set the range for x and y axes
set xrange [0:50]
set yrange [0:50]

# Set the fixed z-coordinate
fixed_z = 25

# Plot the vector field
plot 'monopole_efield_vector.plt' using 1:2:(fixed_z):(column(4)):(column(5)) with vectors head filled size 0.04,20,60 lc rgb "blue" notitle
