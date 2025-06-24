#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

EXEC_CMD="cwltool ../../cwl/containered/workflow.cwl params-containered.yml"

source .cwltool-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark cwltool Docker "$EXEC_CMD"
