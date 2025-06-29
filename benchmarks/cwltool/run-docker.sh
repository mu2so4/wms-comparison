#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

source .cwltool-venv/bin/activate

cwltool ../../cwl/containerized/workflow.cwl params-containerized.yml

set +e
