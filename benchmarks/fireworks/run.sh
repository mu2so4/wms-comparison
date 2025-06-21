#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

if [[ ! -f $LOCKFILE ]]; then
    ./init.sh
fi

source .fireworks-venv/bin/activate

lpad add workflow.yaml
rlaunch -s rapidfire

set +e
