set title "Histogram of equilibration times"
set xlabel "equilibration time"
set ylabel "number of occurrences"

set style data histogram
set boxwidth 0.9

# Use smooth frequency to count occurrences of each unique value
plot "histogram.dat" using 1:($0+1) smooth frequency with boxes notitle
