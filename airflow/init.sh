#!/bin/bash

INIT_FILE="init-complete"

if [[ -f $INIT_FILE ]]; then
    echo "Init already complete. To reinit pleas remove the $INIT_FILE file"
    exit
fi

set -e
set -x

# setup tasks environment
TASK_VENV_PATH="airflow-task-venv"
rm -rf $TASK_VENV_PATH
python3.11 -m venv $TASK_VENV_PATH
source $TASK_VENV_PATH/bin/activate
pip install -r ../requirements.txt
deactivate

# setup CWL scripts
cp ../cwltool/params.yml .
PARAM_PATH=$(realpath params.yml)
cp ../cwltool/main.cwl .
WORKFLOW_PATH=$(realpath main.cwl)
PYTHON_TASK_PATH=$(realpath -s $TASK_VENV_PATH/bin/python)
sed "s#python#${PYTHON_TASK_PATH}#g" ../cwltool/task1.cwl > task1.cwl
sed "s#python#${PYTHON_TASK_PATH}#g" ../cwltool/task2.cwl > task2.cwl

# setup airflow environment
VENV_PATH="airflow-venv"
rm -rf $VENV_PATH
python3.8 -m venv $VENV_PATH
source $VENV_PATH/bin/activate
pip install cwl-airflow==1.2.11 --constraint \
    "https://raw.githubusercontent.com/Barski-lab/cwl-airflow/master/packaging/constraints/constraints-3.8.txt"


AIRFLOW_HOME="$HOME/airflow"
rm -rf "${AIRFLOW_HOME}"

cwl-airflow init
airflow users create \
    --username admin \
    --password admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com

sed "s#AIRFLOW_HOME#${AIRFLOW_HOME}#g" cwl-airflow.cfg >> "${AIRFLOW_HOME}/airflow.cfg"
sed "s#WORKFLOW_PATH#${WORKFLOW_PATH}#g" seismic_demo.py | sed "s#PARAM_PATH#${PARAM_PATH}#g" > ${AIRFLOW_HOME}/dags/seismic_demo.py

touch $INIT_FILE

set +x
set +e

echo "Apache Airflow with CWL-Airflow initialization complete successfully!"
