#!/bin/bash

VENV_PATH='.snakemake-venv'

set -e


if [ ! -d $VENV_PATH ]; then
    echo "Creating the Snakemake virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The Snakemake virtual environment already exists. Initialization of venv skipped."
fi

source $VENV_PATH/bin/activate
pip install snakemake==9.3.3
pip install -r ../requirements.txt

set +e

echo
echo "Snakemake initialized successfully!"
echo
echo "To run workflow in the Snakefile file, run"
echo "snakemake --cores 1"
