#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: $0 tag"
    exit 1
fi

cd $(dirname "$0")

cp ../../src/task2.py .

docker build -t seismic-processing-task:$1 .

rm task2.py
