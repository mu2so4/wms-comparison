#!/bin/bash

ITERATION_COUNT=15
TIMEFORMAT=%3R

source .fireworks-venv/bin/activate

OUT_FILE=time0.txt

>$OUT_FILE

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    rm -f outputs/filtered2.sd outputs/out_fin.png outputs/filtered.segy
    echo "iteration $i of $ITERATION_COUNT"
    lpad add workflow.yaml

    { time rlaunch -s rapidfire ; } 2>&1 >/dev/null | tail -1 >>$OUT_FILE
    rm -rf launcher*
done


sed "s#,#.#g" $OUT_FILE > time.txt

rm $OUT_FILE
