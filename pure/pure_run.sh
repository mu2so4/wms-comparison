#!/bin/bash

set -e

source .pure-venv/bin/activate

ITERATION_COUNT=15
TIMEFORMAT=%R

OUT_FILE=time0.txt

>$OUT_FILE

for ((i = 1; i <= 3; i++)); do
    echo "IDLE iteration $i of 3"
    python pure_workflow.py
done

echo

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    echo "iteration $i of $ITERATION_COUNT"
    { time python pure_workflow.py; } 2>>$OUT_FILE
done


sed "s#,#.#g" $OUT_FILE > time.txt

rm $OUT_FILE

python ../stats.py time.txt
