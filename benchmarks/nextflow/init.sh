#!/bin/bash

WMS="Nextflow"
VENV_PATH=".nextflow-venv"
LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e

curl -s https://get.nextflow.io | bash

sudo mv nextflow /usr/local/bin/



if [ ! -d $VENV_PATH ]; then
    echo "Creating the ${WMS} virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The ${WMS} virtual environment already exists. Initialization of venv skipped."
fi

source {$VENV_PATH}/bin/activate
pip install -r ../requirements.txt
pip install -r requirements.txt

echo "Converting CWL to ${WMS}"
janis translate --from cwl --to nextflow ../cwltool/main.cwl

touch $LOCKFILE

set +e

echo "${WMS} initialized successfully!"
echo
echo "Run it to submit task to ${WMS}"
echo "source $VENV_PATH/bin/activate"
echo "nextflow run main.nf"
