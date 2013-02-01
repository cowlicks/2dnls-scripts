#! /bin/bash
# This script is for scanning in p/pcr.

mkdir ppcr_scan
rm ppcr_scan/*

for (( i=1; i <= 9; i++ ))
do
   # Clean.
   rm out/*
   rm bin/*
   rm out.*.png
   # Edit the beam coordinates in parammod.
   sed -i -e"s/Ppcr0 \= .*\..*d0/Ppcr0 = 0.${i}d0/" src/parammod.f90
   sed -i -e"s/Ppcr1 \= .*\..*d0/Ppcr1 = 0.${i}d0/" src/parammod.f90
   # Run.
   make
   ./bin/nls.e
   octave plotnlsdata.m
   # Saves the first image of the simulation in the spread_scan/ dir.
   mkdir ppcr_scan/ppcr_0.${i}
   mv out.*.png ppcr_scan/ppcr_0.${i}/
done

