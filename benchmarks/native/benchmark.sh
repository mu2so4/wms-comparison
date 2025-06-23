#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

run_bench() {
    python native_workflow.py ../../inputs/input.sgy 15 30 20 interm.sd 40 50 pic.png result.segy
}

source .native-venv/bin/activate

ITERATION_COUNT=15
TIMEFORMAT=%R

OUT_FILE=time0.txt

for ((i = 1; i <= 3; i++)); do
    echo "IDLE iteration $i of 3"
    run_bench
done

echo

echo "Native" >$OUT_FILE
echo "Local" >>$OUT_FILE

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    echo "iteration $i of $ITERATION_COUNT"
    { time run_bench; } 2>>$OUT_FILE
done

mkdir -p ../../results
sed "s#,#.#g" $OUT_FILE > ../../results/native-local.txt

rm $OUT_FILE

python ../../stats.py ../../results/native-local.txt
