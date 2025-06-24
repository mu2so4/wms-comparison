#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

EXEC_CMD="python native_workflow.py ../../inputs/input.sgy 15 30 20 interm.sd 40 50 pic.png result.segy"

source .native-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Native Local "$EXEC_CMD"
