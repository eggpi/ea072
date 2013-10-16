#!/bin/bash

for i in `seq 1 1 1000`;
do
    echo "Running instance $i"
    python tsp.py $1 output/debug$i output/out$i
done;
