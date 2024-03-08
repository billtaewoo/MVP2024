set title "Infection fraction against Immune fraction"
set xlabel "Immune fraction"
set ylabel "Infection fraction"
set xrange [0:1]
set yrange [0:0.3]
plot "immuneplot.dat" with lines
