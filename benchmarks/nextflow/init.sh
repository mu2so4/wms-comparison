#!/bin/bash

cd $(dirname "$0")

WMS="Nextflow"
VENV_PATH=".nextflow-venv"
LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e


if [ ! -d $VENV_PATH ]; then
    echo "Creating the ${WMS} virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The ${WMS} virtual environment already exists. Initialization of venv skipped."
fi

source $VENV_PATH/bin/activate
pip install -r ../../requirements.txt
pip install -r requirements.txt


if [[ ! -f bin/nextflow ]]; then
    mkdir -p temp
    cd temp
    curl -s https://get.nextflow.io | bash
    cd ..
    mkdir -p bin
    mv temp/nextflow bin/nextflow
    rm -rf temp/
fi

INPUT_FILE=$(realpath ../../inputs/input.sgy)
SRC_DIR=$(realpath ../../src/)

cd native

sed "s#INPUT_FILE#${INPUT_FILE}#g" nextflow-draft.config > nextflow.config
sed "s#SRC_PATH#${SRC_DIR}#g" task1-draft.nf > task1.nf
sed "s#SRC_PATH#${SRC_DIR}#g" task2-draft.nf > task2.nf

cd ../apptainer
sed "s#INPUT_FILE#${INPUT_FILE}#g" nextflow-draft.config > nextflow.config

cd ..

touch $LOCKFILE

set +e

echo "${WMS} initialized successfully!"
echo
echo "Run it to submit task to ${WMS}"
echo "source $VENV_PATH/bin/activate"
echo "./bin/nextflow run main.nf"
