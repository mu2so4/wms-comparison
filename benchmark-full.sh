#!/bin/bash

cd $(dirname "$0")


rm -rf results

mkdir -p results

BENCHMARKS=$(find benchmarks/*/benchmark*.sh)
BENCHMARK_COUNT=$(find benchmarks/*/benchmark*.sh | wc -l)

INDEX=1
for BENCHMARK in $BENCHMARKS; do
    echo "Benchmark $INDEX of $BENCHMARK_COUNT: $BENCHMARK"
    bash $BENCHMARK
    INDEX=$(expr ${INDEX} + 1)
done

set -e

source benchmarks/native/.native-venv/bin/activate # workaround to obtain the Matplotlib dependency

python summary.py
