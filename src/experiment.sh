#!/bin/bash

arrivalRates=( 100 1000 10000 100000 )
deletionRates=( 10 20 30 40 50 )
TIME=60
BFSIZE=256
BFHASHES=3
RANDOMSIZE=100

for ar in "${arrivalRates[@]}"
do
    for dr in "${deletionRates[@]}"
    do
        python decayer.py $TIME $BFSIZE $BFHASHES 1 $ar $dr $RANDOMSIZE
    done
done

