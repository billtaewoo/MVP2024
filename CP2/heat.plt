set title "Heatmap of probability 1 and 3"
set xlabel "probability 3"
set ylabel "probability 1"
set xrange [0:1]
set yrange [0:1]
set size ratio -1
plot "heatmap1.dat" with image
