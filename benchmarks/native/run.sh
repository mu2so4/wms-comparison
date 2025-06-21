#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

if [[ ! -f $LOCKFILE ]]; then
    ./init.sh
fi

source .native-venv/bin/activate

python native_workflow.py ../../inputs/input.sgy 15 30 20 interm.sd 40 50 pic.png result.segy

set +e
