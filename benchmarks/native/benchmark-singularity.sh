#!/bin/bash

cd $(dirname "$0")

set -e

INPUT_PATH=$PWD/../../inputs
TASK1_OUT=$PWD/out-singularity-task1
TASK2_OUT=$PWD/out-singularity-task2

mkdir -p $TASK1_OUT
mkdir -p $TASK2_OUT

SINGULARITY_FILTER_CMD="singularity run \
    --mount type=bind,src=${INPUT_PATH},dst=/app/data,ro \
    --mount type=bind,src=${TASK1_OUT},dst=/app/outputs \
    docker://mu2so4/seismic-filter-task:1.0.2 \
    /app/data/input.sgy 15 30 20 /app/outputs/interm.sd"

SINGULARITY_PROCESS_CMD="singularity run \
    --mount type=bind,src=${TASK1_OUT},dst=/app/data,ro \
    --mount type=bind,src=${TASK2_OUT},dst=/app/outputs \
    docker://mu2so4/seismic-processing-task:1.0.2 \
    /app/data/interm.sd 40 50 /app/outputs/pic.png /app/outputs/result.segy"

FULL_CMD="${SINGULARITY_FILTER_CMD} && ${SINGULARITY_PROCESS_CMD}"

source ../benchmark-utils.sh
run_benchmark Native Docker "$FULL_CMD"
