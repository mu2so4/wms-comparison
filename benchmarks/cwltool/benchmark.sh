#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

EXEC_CMD="cwltool ../../cwl/native/workflow.cwl params.yml"

source .cwltool-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Cwltool Local "$EXEC_CMD"
