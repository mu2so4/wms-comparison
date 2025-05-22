#!/bin/bash

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e

VENV_PATH=".fireworks-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the FireWorks virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The FireWorks virtual environment already exists. Initialization of venv skipped."
fi


source $VENV_PATH/bin/activate

pip install -r requirements.txt
mkdir -p ~/.fireworks
echo MONGOMOCK_SERVERSTORE_FILE: $HOME/.fireworks/mongomock.json > ~/.fireworks/FW_config.yaml
echo '{}' > ~/.fireworks/mongomock.json
lpad reset --password="$(date +%Y-%m-%d)"

pip install -r ../requirements.txt

OUTPUT_DIR=$(realpath outputs)
REPO_DIR=$(realpath ..)

sed "s#OUTPUT_DIR#${OUTPUT_DIR}#g" workflow-draft.yaml | \
    sed "s#REPO_DIR#${REPO_DIR}#g" > workflow.yaml

touch $LOCKFILE

set +e

echo "FireWorks initialized successfully!"
echo
echo "Run it to submit task to the FireWorks:"
echo "source $VENV_PATH/bin/activate"
echo "lpad add workflow.yaml"
echo "rlaunch -s rapidfire"
