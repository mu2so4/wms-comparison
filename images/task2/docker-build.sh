#!/bin/bash

cd $(dirname "$0")

cp ../../src/task2.py .

docker build -t seismic-filter-task:test .

rm task2.py
