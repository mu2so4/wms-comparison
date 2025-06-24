#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

./init.sh

source .cwltool-venv/bin/activate

cwltool --singularity ../../cwl/containered/workflow.cwl params-containered.yml

set +e
