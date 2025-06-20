#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: $0 tag"
    exit 1
fi

cd $(dirname "$0")

cp ../../src/task1.py .

docker build -t seismic-filter-task:$1 .

rm task1.py
