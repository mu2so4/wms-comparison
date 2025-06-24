#!/bin/bash

cd $(dirname "$0")

set -e

INPUT_PATH=$PWD/../../inputs
TASK1_OUT=$PWD/out-docker-task1
TASK2_OUT=$PWD/out-docker-task2

DOCKER_FILTER_CMD="docker run \
    -v ${INPUT_PATH}:/app/data \
    -v ${TASK1_OUT}:/app/outputs \
    mu2so4/seismic-filter-task:1.0.2 \
    /app/data/input.sgy 15 30 20 /app/outputs/interm.sd"

DOCKER_PROCESS_CMD="docker run \
    -v ${TASK1_OUT}:/app/data \
    -v ${TASK2_OUT}:/app/outputs \
    mu2so4/seismic-processing-task:1.0.2 \
    /app/data/interm.sd 40 50 /app/outputs/pic.png /app/outputs/result.segy"


FULL_CMD="${DOCKER_FILTER_CMD} && ${DOCKER_PROCESS_CMD}"


source ../benchmark-utils.sh
run_benchmark Native Docker "$FULL_CMD"
