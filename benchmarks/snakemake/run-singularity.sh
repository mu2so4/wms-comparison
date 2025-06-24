#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

source .snakemake-venv/bin/activate

cd container
snakemake --cores 1 --use-apptainer --singularity-args "-B $(realpath ../../../inputs),$(pwd)"

set +e
