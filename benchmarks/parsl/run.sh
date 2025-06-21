#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

if [[ ! -f $LOCKFILE ]]; then
    ./init.sh
fi

mkdir -p out

source .parsl-venv/bin/activate

python workflow.py

set +e
