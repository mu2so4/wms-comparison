#!/bin/bash

cd $(dirname "$0")

set -e

./init.sh

source .parsl-venv/bin/activate

python workflow-docker.py

set +e
