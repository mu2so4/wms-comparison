#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

EXEC_CMD="cwltool ../../cwl/containerized/workflow.cwl params-containerized.yml"

source .cwltool-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Cwltool Docker "$EXEC_CMD"
