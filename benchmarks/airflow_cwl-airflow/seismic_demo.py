from cwl_airflow.extensions.cwldag import CWLDAG

default_args = {
    "params": {
        "job": "PARAM_PATH"
    }
}

dag = CWLDAG(
    workflow="WORKFLOW_PATH",
    dag_id="seismic",
    default_args=default_args
)
