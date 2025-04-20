#!/bin/bash

INIT_FILE="init-complete"

if [[ -f $INIT_FILE ]]; then
    echo "Init already complete. To reinit pleas remove the $INIT_FILE file"
    exit
fi

set -x
python3.8 -m venv airflow-venv
source airflow-venv/bin/activate
pip install cwl-airflow==1.2.11 --constraint \
    "https://raw.githubusercontent.com/Barski-lab/cwl-airflow/master/packaging/constraints/constraints-3.8.txt"

AIRFLOW_HOME="$HOME/airflow"
rm -rf "$AIRFLOW_HOME"

cwl-airflow init
airflow users create \
    --username admin \
    --password admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com

sed "s/AIRFLOW_HOME/$AIRFLOW_HOME/g" cwl-airfow.cfg >> "$AIRFLOW_HOME/airflow.cfg"

cp seismic_demo.py $AIRFLOW_HOME/dags

touch $INIT_FILE

set +x
