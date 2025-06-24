#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

CLEAN_CMD=""
EXEC_CMD="snakemake --quiet -F --cores 1"

source .snakemake-venv/bin/activate
source ../benchmark-utils.sh

run_benchmark Snakemake Local "$EXEC_CMD" "$CLEAN_CMD"
