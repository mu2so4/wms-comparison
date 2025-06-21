#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

if [[ ! -f $LOCKFILE ]]; then
    ./init.sh
fi

source .nextflow-venv/bin/activate

./bin/nextflow run apptainer/main.nf

set +e
