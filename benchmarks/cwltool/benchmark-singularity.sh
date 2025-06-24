#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

EXEC_CMD="cwltool --singularity ../../cwl/containered/workflow.cwl params-containered.yml"

source .cwltool-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark cwltool Singularity "$EXEC_CMD"
