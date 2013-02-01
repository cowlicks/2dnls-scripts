#! /bin/bash
# Show the laser at the entrance to the plasma.

# Clean
rm out/*
rm bin/*
# Edit the pz parameter in parammod.f90
sed -i -e"s/Zf \= .*\..*d.*/Zf = 0.0d0/" src/parammod.f90
# Run the simulation.
make
./bin/nls.e
octave plotnlsdata.m
eog out.0000.png

