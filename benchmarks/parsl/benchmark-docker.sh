#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD="sudo rm -rf out*"
EXEC_CMD="python workflow-docker.py"

source .parsl-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Parsl Docker "$EXEC_CMD" "$CLEAN_CMD"
