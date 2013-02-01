# Clean the 2dnls output on the remote macine.
ssh cowlicks@linux7.ph.utexas.edu 'bash -s' << 'ENDSSH'
rm -r ~/2dnls/bin/* ~/2dnls/out/* ~/2dnls/src/*
ENDSSH

# Transfer the code.
scp -r ~/2dnls/analysis.py ~/2dnls/lib/ ~/2dnls/Makefile ~/2dnls/src/ cowlicks@linux7.ph.utexas.edu:~/2dnls/.

# Create directories needed, build, then run.
ssh cowlicks@linux7.ph.utexas.edu 'bash -s' << 'ENDSSH'
export PYTHONPATH=$HOME/local/lib64/python2.4/site-packages
mkdir ~/2dnls/bin ~/2dnls/out
cd ~/2dnls/
make
./bin/nls.e
python analysis.py
DATE=`date +%F:%R:%S`
mkdir -p ~/2dnls/data/$DATE
cp ~/2dnls/src/parammod.f90 ~/2dnls/data/$DATE/.
cp ~/2dnls/*.png ~/2dnls/data/$DATE/.
ENDSSH

# Copy the results back to my machine.
mkdir ~/2dnls/data/
scp -r cowlicks@linux7.ph.utexas.edu:~/2dnls/data/. ~/2dnls/data/.
