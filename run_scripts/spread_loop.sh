#! /bin/bash
# This script is for scanning in the distance between the two beams. It
# is designed only to look at the first image, right where the beam
# enters the plasma.

# i is the distance of the center of the beam from an axis in rayleigh
# lengths. So the actual distance between the beams is sqrt(2)*2*i.
for (( i=1; i <= 9; i++ ))
do
   # Clean.
   rm out/*
   rm bin/*
   # Edit the beam coordinates in parammod.
   sed -i -e"s/xo0 \= -0\..*d0\, xo1 \= 0\..*d0/xo0 = -0.${i}d0, xo1 = 0.${i}d0/" src/parammod.f90
   # Run.
   make
   ./bin/nls.e
   octave plotnlsdata.m
   # Saves the first image of the simulation in the spread_scan/ dir.
   mv out.0000.png spread_scan/xo0$i.png
done

