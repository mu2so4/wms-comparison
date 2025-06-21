#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: $0 cwl-file"
    exit 1
fi


echo "Converting CWL to Nextflow"
janis translate --from cwl --to nextflow $1
