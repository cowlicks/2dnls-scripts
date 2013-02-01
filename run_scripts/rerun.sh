#! /bin/bash
# Script to rerun the simulation. It cleans, runs the simulation,
# creates the images in matlab/octave, then makes gif and displays it.

echo "Cleaning"
rm bin/*
rm out.*.png

echo "Making"
make

echo "Running"
./bin/nls.e

echo "Running matlab script"
octave plotnlsdata.m

eog out.0000.png
#echo "Making gif"
#convert -delay 30 -loop 0 out.*.*png animation.gif

#notify-send 'I am done crunching data.'

#echo "Showing"
#gwenview animation.gif
