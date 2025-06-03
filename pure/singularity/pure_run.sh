#!/bin/bash

ITERATION_COUNT=15
TIMEFORMAT=%R

OUT_FILE=time0.txt

>$OUT_FILE

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    echo "iteration $i of $ITERATION_COUNT"
    { time ./run.sh ; } 2>>$OUT_FILE
done


sed "s#,#.#g" $OUT_FILE > time.txt

rm $OUT_FILE
