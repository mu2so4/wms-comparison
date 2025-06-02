#!/bin/bash

INPUT_PATH=$PWD/../../inputs
TASK1_OUT=$PWD/out-task1
TASK2_OUT=$PWD/out-task2

singularity run \
    --mount type=bind,src=${INPUT_PATH},dst=/app/data,ro \
    --mount type=bind,src=${TASK1_OUT},dst=/app/outputs \
    ../../containers/docker-task1/task1.sif \
    /app/data/input.sgy 15 30 20 /app/outputs/interm.sd && \
    
singularity run \
    --mount type=bind,src=${TASK1_OUT},dst=/app/data,ro \
    --mount type=bind,src=${TASK2_OUT},dst=/app/outputs \
    ../../containers/docker-task2/task2.sif \
    /app/data/interm.sd 40 50 /app/outputs/pic.png /app/outputs/result.segy
