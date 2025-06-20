#!/bin/bash

cd $(dirname "$0")

cp ../../src/task1.py .

docker build -t seismic-filter-task:test .

rm task1.py
