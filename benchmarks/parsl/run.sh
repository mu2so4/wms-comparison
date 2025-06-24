#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

set -e

./init.sh

mkdir -p out

source .parsl-venv/bin/activate

python workflow.py

set +e
