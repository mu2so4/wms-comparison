from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.models.param import Param

# Define the path to your Python scripts.
# IMPORTANT: These paths must be accessible by the Airflow worker executing the task.
# You might need to adjust these paths based on your Airflow environment setup.
TASK1_SCRIPT = "TASK1_PATH"
TASK2_SCRIPT = "TASK2_PATH"

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': pendulum.duration(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'default_pool',
    # 'priority_weight': 10,
    # 'end_date': datetime(2023, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success',
}

with DAG(
    dag_id="seismic",
    # Define the schedule for the DAG. Use None for manual runs, or a cron expression.
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["seismic", "cwl", "example"],
    default_args=default_args,
    # Define DAG parameters corresponding to CWL inputs
    params={
        "inpFile": Param(type="string", description="Input data file path for task1"),
        "f1": Param(type="integer", description="Parameter f1 for task1"),
        "f2": Param(type="integer", description="Parameter f2 for task1"),
        "freq": Param(type="integer", description="Parameter freq for task1"),
        "freq2": Param(type="integer", description="Parameter freq2 for task2"),
        "freq3": Param(type="integer", description="Parameter freq3 for task2"),
        "out_stage1": Param(type="string", description="Output file path for stage1 (input to task2)"),
        "out_pic": Param(type="string", description="Output picture file path for stage2"),
        "out_segy": Param(type="string", description="Output segy file path for stage2"),
    },
) as dag:
    # Stage 1: Runs task1.py
    # This task corresponds to the 'stage1' CommandLineTool in the CWL.
    # It takes parameters and writes output to the path specified by {{ params.out_stage1 }}.
    stage1_task = BashOperator(
        task_id="stage1",
        bash_command=(
            f"python {TASK1_SCRIPT} "
            "{{ params.inpFile }} "
            "{{ params.f1 }} "
            "{{ params.f2 }} "
            "{{ params.freq }} "
            "TEMP_PATH/{{ params.out_stage1 }}" # This parameter defines the output path for stage1
        ),
        # Assumption: task1.py accepts arguments in the specified order and writes its output
        # to the path provided as the 5th argument.
        # stdout will be captured by Airflow logs by default.
    )

    # Stage 2: Runs task2.py
    # This task corresponds to the 'stage2' CommandLineTool in the CWL.
    # It takes the output path from stage1 as its input filename,
    # and other parameters, writing outputs to paths specified by {{ params.out_pic }} and {{ params.out_segy }}.
    stage2_task = BashOperator(
        task_id="stage2",
        bash_command=(
            f"python {TASK2_SCRIPT} "
            "TEMP_PATH/{{ params.out_stage1 }} " # Input filename for task2 comes from stage1's output path
            "{{ params.freq2 }} "
            "{{ params.freq3 }} "
            "OUT_PATH/{{ params.out_pic }} " # This parameter defines the output picture path for stage2
            "OUT_PATH/{{ params.out_segy }}" # This parameter defines the output segy file path for stage2
        ),
        # Assumption: task2.py accepts arguments in the specified order (input filename, freq2, freq3, outPic, outFile)
        # and reads from the first argument, writing outputs to paths provided as 4th and 5th arguments.
        # stdout will be captured by Airflow logs by default.
    )

    # Define the workflow dependency: stage2 depends on stage1 completing successfully.
    # In CWL, this is implicit via outputSource/in connections. In Airflow, it's explicit.
    stage1_task >> stage2_task

# How to run this DAG:
# 1. Save the code as a Python file (e.g., cwl_workflow_dag.py) in your Airflow DAGs folder.
# 2. Ensure the Python scripts task1.py and task2.py are present at the specified paths
#    (/home/mu2so4/univ/disser/cwl-pure/) on the Airflow worker(s) that will execute the tasks.
# 3. The paths specified in the DAG parameters (e.g., {{ params.inpFile }}) must be accessible
#    for reading by stage1 and for writing by stage1 and stage2, from the perspective of the worker.
#    This often means using shared storage or ensuring paths are valid within a container (if using DockerOperator).
# 4. Enable the DAG in the Airflow UI.
# 5. Trigger the DAG manually. When triggering, you will be prompted to provide the values for the DAG parameters
#    (inpFile, f1, f2, etc.) via a JSON configuration. Example JSON:
#    {
#      "inpFile": "/path/to/your/input.dat",
#      "f1": 10,
#      "f2": 200,
#      "freq": 1000,
#      "freq2": 50,
#      "freq3": 150,
#      "out_stage1": "/path/to/write/filtered.sd",
#      "out_pic": "/path/to/write/output_image.png",
#      "out_segy": "/path/to/write/output.segy"
#    }
# The final output files from the workflow will be located at the paths specified by the
# 'out_pic' and 'out_segy' parameters provided during the DAG run trigger.
