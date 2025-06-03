#!/bin/bash

INPUT_PATH=$PWD/../../inputs
TASK1_OUT=$PWD/out-task1
TASK2_OUT=$PWD/out-task2

docker run \
    -v ${INPUT_PATH}:/app/data \
    -v ${TASK1_OUT}:/app/outputs \
    mu2so4/seismic-filter-task:1.0.1 \
    /app/data/input.sgy 15 30 20 /app/outputs/interm.sd && \
docker run \
    -v ${TASK1_OUT}:/app/data \
    -v ${TASK2_OUT}:/app/outputs \
    mu2so4/seismic-processing-task:1.0.1 \
    /app/data/interm.sd 40 50 /app/outputs/pic.png /app/outputs/result.segy
