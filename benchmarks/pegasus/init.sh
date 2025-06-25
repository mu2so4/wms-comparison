#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To init again remove the '$LOCKFILE' file"
    exit
fi

set -e

VENV_PATH=".pegasus-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the Pegasus virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The Pegasus virtual environment already exists. Initialization of venv skipped."
fi

. /etc/os-release

curl https://download.pegasus.isi.edu/pegasus/gpg.txt | apt-key add -
INSTALL_URL="https://download.pegasus.isi.edu/pegasus/${ID} ${VERSION_CODENAME} main"
echo "deb ${INSTALL_URL}" >/etc/apt/sources.list.d/pegasus.list
apt-get update
apt-get install -y pegasus

source $VENV_PATH/bin/activate
pip install -r requirements.txt
pip install -r ../../requirements.txt

PYTHON_PATH=$(pwd)/bin/python
INPUT_PATH=$(realpath ../../inputs/input.sgy)
TASK1_PATH=$(realpath ../../src/task1.py)
TASK2_PATH=$(realpath ../../src/task2.py)

sed "s#PYTHON_PATH#${PYTHON_PATH}#g" workflow_generator-draft.py | \
    sed "s#INPUT_PATH#${INPUT_PATH}#g" | \
    sed "s#TASK1_PATH#${TASK1_PATH}#g" | \
    sed "s#TASK2_PATH#${TASK2_PATH}#g" > workflow_generator.py

touch $LOCKFILE

set +e

echo
echo "Pegasus workflow initialized successfully!"
#echo
#echo "Run it to run the pure workflow:"
#echo "source $VENV_PATH/bin/activate"
#echo "python -m main StageTwo --local-scheduler"
