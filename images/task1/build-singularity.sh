#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 docker_image_tag"
    exit 1
fi

cd $(dirname "$0")

singularity build task1.sif docker-daemon://$1

