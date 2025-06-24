#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD=""
EXEC_CMD="snakemake --snakefile container/Snakefile --cores 1 --quiet --forceall --use-apptainer --singularity-args \"-B $(realpath ../../inputs),$(pwd)\""

source .snakemake-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Snakemake Local "$EXEC_CMD" "$CLEAN_CMD"
