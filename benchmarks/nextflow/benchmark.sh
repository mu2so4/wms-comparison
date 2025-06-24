#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="rm -rf outputs"
EXEC_CMD="./bin/nextflow run native/main.nf"

source .nextflow-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Nextflow Local "$EXEC_CMD" "$CLEAN_CMD"
