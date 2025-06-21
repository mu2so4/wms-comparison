#!/bin/bash

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e

VENV_PATH=".parsl-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the Parsl virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The Parsl virtual environment already exists. Initialization of venv skipped."
fi


source $VENV_PATH/bin/activate
pip install parsl==2025.5.19 pyyaml==6.0.2
pip install -r ../requirements.txt

cp ../cwltool/params.yml .

touch $LOCKFILE

set +e

echo "Parsl initialized successfully!"
echo
echo "Run it to submit task to the Parsl:"
echo "source $VENV_PATH/bin/activate"
echo "python workflow.py"
