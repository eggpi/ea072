#!/bin/bash

for i in `seq 1 1 1000`;
do
    echo "Running instance $i"
    python numbers.py instancia_numbers.txt output/debug$i output/out$i
done;
