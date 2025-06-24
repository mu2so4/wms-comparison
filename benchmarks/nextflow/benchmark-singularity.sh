#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="rm -rf outputs work"
EXEC_CMD="./bin/nextflow run apptainer/main.nf"

source ../benchmark-utils.sh

run_benchmark Nextflow Singularity "$EXEC_CMD" "$CLEAN_CMD"
