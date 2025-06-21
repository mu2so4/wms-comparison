#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

if [[ ! -f $LOCKFILE ]]; then
    ./init.sh
fi

source .luigi-venv/bin/activate

python -m main StageTwo --local-scheduler

set +e
