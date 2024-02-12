#!/bin/bash

values=(3 5 10 15 20 25 30 35 40 45 50)
for n in "${values[@]}"; do
    data="n=$n"
    start_time=$(date +%s.%N)
    minizinc --solver chuffed -a latin_square.mzn -D "$data" > /dev/null 2>&1
    end_time=$(date +%s.%N)
    computation_time=$(echo "$end_time - $start_time" | bc)
    echo "n = $n, time = $(printf '%0.2f' ${computation_time}) seconds"
    #echo "$solutions" | shuf -n 1
done > results.txt

echo "Results saved to results.txt"

