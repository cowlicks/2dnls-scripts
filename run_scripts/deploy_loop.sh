#! /usr/bin/env bash
# For loop to iterate over some variable:
    # Modify parammod.f90, then send it to remote machine
    # Make, run, analyze.
    # Move the generated images and contents of out/ to local machine
    # in correct local directories which are named uniquely.
    
# Clean locally
# Interval amount.
xinterval=0.05
pinterval=0.1
# Initial values
x0=0
x1=0
pz=0
for (( i=11; i <= 20; i++ ))
do
    # Spread loop.
    x0=`echo "$x0 + $xinterval" | bc`
    x1=`echo "$x1 + $xinterval" | bc`
    # Rewrite parrammod.f90
    echo "rewriting parrammod, spread x0 = 0${x0} x1 = 0${x1}"
    sed -i -e "25s/.*/  real(kind=prec), parameter :: xo0 = 0${x0}d0, xo1 = -0${x1}d0/" ~/2dnls/src/parammod.f90
    for (( j=0; j <= 10; j++))
    do
        # make pz.
        pz=`echo "$pz + $pinterval" | bc`
        # Rewrite parammod.f90
        echo "rewriting pz=${pz} in parammod."
        sed -i -e "16s/.*/  real(kind=prec), parameter :: pz = 0${pz}d0/" ~/2dnls/src/parammod.f90

        # Send parammod.f90
        scp ~/2dnls/src/parammod.f90 cowlicks@linux7.ph.utexas.edu:~/2dnls/src/.
        # Clean, run, and analyze on the remote host.
        echo "Running on remote host."
        ssh -n cowlicks@linux7.ph.utexas.edu 'cd 2dnls; ./run.sh'
        # Transfer the data back to the local machine
        echo "Transfering data back."
        DATADIRNAME=~/2dnls/data/spread`echo $x0*2 | bc`_pz0/
        mkdir $DATADIRNAME
        scp -r cowlicks@linux7.ph.utexas.edu:/temp/cowlicks/2dnls/out/ ${DATADIRNAME}.
        cp ~/2dnls/src/parammod.f90 ${DATADIRNAME}.
    done
done
