#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="rm -rf outputs/filtered2.sd outputs/out_fin.png outputs/filtered.segy launcher*"
EXEC_CMD="lpad add workflow.yaml && rlaunch -s rapidfire"

source .fireworks-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark FireWorks Local "$EXEC_CMD" "$CLEAN_CMD"
