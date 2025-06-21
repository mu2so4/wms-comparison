#!/bin/bash

source .snakemake-venv/bin/activate

ITERATION_COUNT=15
TIMEFORMAT=%R

OUT_FILE=time0.txt

>$OUT_FILE

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    echo "iteration $i of $ITERATION_COUNT"
    { time snakemake --quiet -F --cores 1; } 2>>$OUT_FILE
done


sed "s#,#.#g" $OUT_FILE > time.txt

rm $OUT_FILE
