#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

mkdir -p out

source .parsl-venv/bin/activate

python workflow.py

set +e
