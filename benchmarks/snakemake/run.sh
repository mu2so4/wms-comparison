#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

source .snakemake-venv/bin/activate

snakemake --cores 1

set +e
