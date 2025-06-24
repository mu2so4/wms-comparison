#!/bin/bash

run_benchmark() {
    local wms_name="$1"
    local container_platform="$2"
    local cmd="$3"
    local clean_cache="${4:-}"
    local iteration_count="${5:-15}"
    
    OUT_FILE=time0.txt
    TIMEFORMAT=%R
    
    set -e

    # Warmup run
    for ((i = 1; i <= 3; i++)); do
        echo "warmup iteration $i of 3"
        eval $($clean_cache)
        eval "$cmd"
    done

    echo
    echo "$wms_name" >$OUT_FILE
    echo "$container_platform" >>$OUT_FILE

    # Main run
    for ((i = 1; i <= $iteration_count; i++)); do
        echo "iteration $i of $iteration_count"
        eval $($clean_cache)
        { time eval "$cmd"; } 2>&1 >/dev/null | tail -1 >>$OUT_FILE
    done

    # Result processing
    mkdir -p ../../results
    benchmark_output=../../results/${wms_name}-${container_platform}.txt
    sed "s#,#.#g" "$OUT_FILE" > $benchmark_output
    rm "$OUT_FILE"
    
    python ../../stats.py $benchmark_output
}
