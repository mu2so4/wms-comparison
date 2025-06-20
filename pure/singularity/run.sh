#!/bin/bash

cd $(dirname "$0")

INPUT_PATH=$PWD/../../inputs
TASK1_OUT=$PWD/out-task1
TASK2_OUT=$PWD/out-task2

singularity run \
    --mount type=bind,src=${INPUT_PATH},dst=/app/data,ro \
    --mount type=bind,src=${TASK1_OUT},dst=/app/outputs \
    docker://mu2so4/seismic-filter-task:1.0.2 \
    /app/data/input.sgy 15 30 20 /app/outputs/interm.sd && \
    
singularity run \
    --mount type=bind,src=${TASK1_OUT},dst=/app/data,ro \
    --mount type=bind,src=${TASK2_OUT},dst=/app/outputs \
    docker://mu2so4/seismic-processing-task:1.0.2 \
    /app/data/interm.sd 40 50 /app/outputs/pic.png /app/outputs/result.segy
