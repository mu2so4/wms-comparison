#!/bin/bash

LOCKFILE="lockfile"

if [[ -f $LOCKFILE ]]; then
    echo "Init already complete. To reinit please remove the $LOCKFILE file"
    exit
fi

set -e
set -x

VENV_PATH=".airflow-venv"

if [ ! -d $VENV_PATH ]; then
    echo "Creating the Apache Airflow virtual environment..."
    python3.11 -m venv $VENV_PATH
else
    echo "The Apache Airflow virtual environment already exists. Initialization of venv skipped."
fi


source $VENV_PATH/bin/activate
pip install apache-airflow==2.10.5
pip install -r ../requirements.txt


AIRFLOW_HOME="$HOME/airflow"
rm -rf "${AIRFLOW_HOME}"

airflow db migrate
airflow users create \
    --username admin \
    --password admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com

TASK1_PATH=$(realpath ../task1.py)
TASK2_PATH=$(realpath ../task2.py)

TEMP_PATH=${AIRFLOW_HOME}/temp
OUT_PATH=${AIRFLOW_HOME}/out
DAG_PATH=${AIRFLOW_HOME}/dags
mkdir $TEMP_PATH
mkdir $OUT_PATH
mkdir $DAG_PATH


sed "s#TASK1_PATH#${TASK1_PATH}#g" dag-draft.py | \
    sed "s#TASK2_PATH#${TASK2_PATH}#g" | \
    sed "s#TEMP_PATH#${TEMP_PATH}#g" | \
    sed "s#OUT_PATH#${OUT_PATH}#g" \
    > ${DAG_PATH}/seismic_demo.py

touch $LOCKFILE

set +x
set +e

echo "Apache Airflow and initialized successfully!"
echo
echo "To deploy Apache Airflow, do this:"
echo "In terminal 1:"
echo "source $VENV_PATH/bin/activate"
echo "airflow scheduler"
echo
echo "In terminal 2:"
echo "source $VENV_PATH/bin/activate"
echo "airflow webserver"
echo
echo "Now you can open Airflow at localhost:8080"
