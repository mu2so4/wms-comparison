#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e

VENV_PATH=".dask-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the Dask virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The Dask virtual environment already exists. Initialization of venv skipped."
fi


source $VENV_PATH/bin/activate
pip install -r requirements.txt
pip install -r ../../requirements.txt

touch $LOCKFILE

set +e

echo
echo "Pure workflow initialized successfully!"
echo
echo "Run it to run the pure workflow:"
echo "source $VENV_PATH/bin/activate"
echo "jupyter lab"
