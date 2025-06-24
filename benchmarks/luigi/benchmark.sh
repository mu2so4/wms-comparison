#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="rm -f filtered2.sd out_fin.png filtered.segy"
EXEC_CMD="python -m main StageTwo --local-scheduler"

source .luigi-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark FireWorks Local "$EXEC_CMD" "$CLEAN_CMD"
