#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="rm -f filtered2.sd out_fin.png filtered.segy"
EXEC_CMD="python workflow.py"

source .parsl-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Parsl Local "$EXEC_CMD" "$CLEAN_CMD"
