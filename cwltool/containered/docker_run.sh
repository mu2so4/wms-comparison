#!/bin/bash

set -e

source ../cwltool-venv/bin/activate

ITERATION_COUNT=15
TIMEFORMAT=%3R

OUT_FILE=time0.txt

>$OUT_FILE

for ((i = 1; i <= 3; i++)); do
    echo "IDLE iteration $i of 3"
    cwltool main.cwl params.yml
done

echo

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    echo "iteration $i of $ITERATION_COUNT"
    { time cwltool main.cwl params.yml ; } 2>&1 >/dev/null | tail -1 >>$OUT_FILE
done


sed "s#,#.#g" $OUT_FILE > time.txt

rm $OUT_FILE

python ../../stats.py time.txt
