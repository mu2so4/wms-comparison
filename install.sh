#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Installation of all WMS already complete. To init over remove the $LOCKFILE file"
    exit
fi

INSTALL_LIST=$(find benchmarks/*/init.sh)
INSTALL_COUNT=$(find benchmarks/*/init.sh | wc -l)

INDEX=1
for INSTALL_CMD in $INSTALL_LIST; do
    echo
    echo '-----------------------------------------------------------------------'
    echo "Installation $INDEX of $INSTALL_COUNT: $INSTALL_CMD"
    echo '-----------------------------------------------------------------------'
    echo
    bash $INSTALL_CMD
    INDEX=$(expr ${INDEX} + 1)
done

touch $LOCKFILE
