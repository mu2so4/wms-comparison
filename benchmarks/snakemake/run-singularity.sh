#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

if [[ ! -f $LOCKFILE ]]; then
    ./init.sh
fi

source .snakemake-venv/bin/activate

cd container
snakemake --cores 1 --use-apptainer --singularity-args "-B $(realpath ../../../inputs),$(pwd)"

set +e
