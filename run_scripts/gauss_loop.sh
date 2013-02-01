#! /bin/bash
# This is a bash script for scanning in pz (pz is the distance the 
# beams propagate before entering the plasma). Only the first image of
# the beam, right as it enters the plasma, is saved for each step.

# i is the step size integers of rayleigh lengths.
for (( i=1; i <= 100; i++ ))
do
   # Clean
   rm out/*
   rm bin/*
   # Edit the pz parameter in parammod.f90
   sed -i -e"s/pz \= .*\.0d0/pz = ${i}.0d0/" src/parammod.f90
   # Run the simulation.
   make
   ./bin/nls.e
   octave plotnlsdata.m
   # This step saves the first image of the simulation and moves it to
   # the gauss_scan/ directory
   mv out.0000.png gauss_scan/pz$i.png
done

