#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="rm -rf out*"
EXEC_CMD="python workflow-singularity.py"

source .parsl-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Parsl Singularity "$EXEC_CMD" "$CLEAN_CMD"
