#!/usr/bin/env python3
from cwl_airflow.extensions.cwldag import CWLDAG
dag = CWLDAG(
    workflow="/home/mu2so4/univ/disser/cwl-pure/cwltool/main.cwl",
    dag_id="seismic"
)
