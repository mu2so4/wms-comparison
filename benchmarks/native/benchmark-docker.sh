#!/bin/bash

cd $(dirname "$0")

set -e

INPUT_PATH=$PWD/../../inputs
TASK1_OUT=$PWD/out-docker-task1
TASK2_OUT=$PWD/out-docker-task2

run_bench() {
    docker run \
        -v ${INPUT_PATH}:/app/data \
        -v ${TASK1_OUT}:/app/outputs \
        mu2so4/seismic-filter-task:1.0.2 \
        /app/data/input.sgy 15 30 20 /app/outputs/interm.sd && \
    docker run \
        -v ${TASK1_OUT}:/app/data \
        -v ${TASK2_OUT}:/app/outputs \
        mu2so4/seismic-processing-task:1.0.2 \
        /app/data/interm.sd 40 50 /app/outputs/pic.png /app/outputs/result.segy
}


for ((i = 1; i <= 3; i++)); do
    echo "IDLE iteration $i of 3"
    run_bench
done

echo

ITERATION_COUNT=15
TIMEFORMAT=%R
OUT_FILE=time0.txt
echo "Native" >$OUT_FILE
echo "Docker" >>$OUT_FILE

for ((i = 1; i <= $ITERATION_COUNT; i++)); do
    echo "iteration $i of $ITERATION_COUNT"
    { time run_bench; } 2>>$OUT_FILE
done

mkdir -p ../../results
sed "s#,#.#g" $OUT_FILE > ../../results/native-docker.txt
python3.11 ../../stats.py ../../results/native-docker.txt

rm $OUT_FILE

