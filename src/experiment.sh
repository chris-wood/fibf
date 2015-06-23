#!/bin/bash

TIME=60
arrivalRates=( 100 1000 10000 100000 )
deletionRates=( 10 20 30 40 50 )
bfsizes=( 128 192 256 )
bfhashes=( 3 4 5 6 7 8 )
RANDOMSIZE=100

for ar in "${arrivalRates[@]}"
do
    for dr in "${deletionRates[@]}"
    do
        for bfsize in "${bfsizes[@]}"
        do
            for bfhash in "${bfhashes[@]}"
            do
                python decayer.py $TIME $bfsize $bfhash 1 $ar $dr $RANDOMSIZE > out_$TIME_$bfsize_$bfhash_1_$ar_$dr_$RANDOMSIZE.out
            done    
        done
    done
done

