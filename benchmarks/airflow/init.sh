#!/bin/bash

cd $(dirname "$0")

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To reinit please remove the $LOCKFILE file"
    exit
fi

set -e

VENV_PATH=".airflow-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the Apache Airflow virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The Apache Airflow virtual environment already exists. Initialization of venv skipped."
fi


source $VENV_PATH/bin/activate
pip install apache-airflow==2.10.5 --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.11.txt
pip install -r ../../requirements.txt


AIRFLOW_HOME="$HOME/airflow"
rm -rf ${AIRFLOW_HOME}
mkdir -p "${AIRFLOW_HOME}"


TASK1_PATH=$(realpath ../../src/task1.py)
TASK2_PATH=$(realpath ../../src/task2.py)

TEMP_PATH=${AIRFLOW_HOME}/temp
OUT_PATH=${AIRFLOW_HOME}/out
DAG_PATH=${AIRFLOW_HOME}/dags
mkdir -p $TEMP_PATH
mkdir -p $OUT_PATH
mkdir -p $DAG_PATH


sed "s#TASK1_PATH#${TASK1_PATH}#g" dag-draft.py | \
    sed "s#TASK2_PATH#${TASK2_PATH}#g" | \
    sed "s#TEMP_PATH#${TEMP_PATH}#g" | \
    sed "s#OUT_PATH#${OUT_PATH}#g" \
    > ${DAG_PATH}/seismic_demo.py

touch $LOCKFILE

set +e

echo "Apache Airflow initialized successfully!"
echo
echo "To deploy Apache Airflow, do this:"
echo "source $VENV_PATH/bin/activate"
echo "airflow standalone"
echo
echo "Then you can open Airflow at localhost:8080 after deployment"
