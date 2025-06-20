#!/bin/bash

cd $(dirname "$0")

set -e

source .pure-venv/bin/activate

python pure_workflow.py

set +e
