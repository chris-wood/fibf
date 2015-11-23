#!/bin/bash

<<<<<<< HEAD
# experiment time
TIME=1000
=======
TIME=3600
>>>>>>> 4ccc88aa63a4fd71c154c2bcfb14c14144ffc0d9

# assuming average 14 hops per link so arrivalRates is for each hop up to middle of the network
# which are assumed to be core routers
arrivalRates=( 28.45 142.25 711.25 3556.25 17781.25 88906.25 444531.25 )
deletionRates=( 10 ) #20 30 40 50 )
bfsizes=( 1024 ) #2048 4096 )
RANDOMSIZE=100
decayRate=1000

for ar in "${arrivalRates[@]}"
do
    for dr in "${deletionRates[@]}"
    do
        for bfsize in "${bfsizes[@]}"
        do
            echo python decayer.py $TIME $bfsize $decayRate $ar $dr $RANDOMSIZE
            OUTFILE="out_${TIME}_${bfsize}_${decayRate}_${ar}_${dr}_${RANDOMSIZE}.out"
            echo ... to $OUTFILE
            python decayer.py $TIME $bfsize $decayRate $ar $dr $RANDOMSIZE > $OUTFILE
        done
    done
done
