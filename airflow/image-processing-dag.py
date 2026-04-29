from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.models.param import Param

# Define the path to your Python scripts.
# IMPORTANT: These paths must be accessible by the Airflow worker executing the task.
# You might need to adjust these paths based on your Airflow environment setup.
CROP_SCRIPT = "CROP_PATH"
SOBEL_SCRIPT = "SOBEL_PATH"
BINARIZE_SCRIPT = "BINARIZE_PATH"
HEIGHT_SCRIPT = "HEIGHT_PATH"

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': pendulum.duration(minutes=5)
}

with DAG(
    dag_id="image-processing",
    # Define the schedule for the DAG. Use None for manual runs, or a cron expression.
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["image processing", "example"],
    default_args=default_args,
    # Define DAG parameters corresponding to CWL inputs
    params={
        "inpFile": Param(type="string", description="Input data file path for crop"),
        "start_x": Param(type="integer", description="Parameter start_x for crop"),
        "start_y": Param(type="integer", description="Parameter start_y for crop"),
        "crop_x": Param(type="integer", description="Parameter crop_x for crop"),
        "crop_y": Param(type="integer", description="Parameter crop_y for crop"),
        "output_file_crop": Param(type="string", description="Output file path for crop (input to sobel)"),
        "output_file_sobel": Param(type="string", description="Output file for sobel (input to binarize)"),
        "thresh": Param(type="integer", description="Parameter thresh for binarize"),
        "output_file_binarize": Param(type="string", description="Output file path for binarize (input to height)"),
        "output_file_hegiht": Param(type="string", description="Output file path for height with final image"),
        "output_height": Param(type="string", description="Output file path for height with final value"),
    },
) as dag:
    # Stage 1: Runs crop.py
    crop_task = BashOperator(
        task_id="crop",
        bash_command=(
            f"python3 {CROP_SCRIPT} "
            "{{ params.inpFile }} "
            "{{ params.start_x }} "
            "{{ params.start_y }} "
            "{{ params.crop_x }} "
            "{{ params.crop_y }} "
            "TEMP_PATH/{{ params.output_file_crop }}" # This parameter defines the output path for crop
        ),
    )

    # Stage 2: Runs sobel.py
    sobel_task = BashOperator(
        task_id="sobel",
        bash_command=(
            f"python3 {SOBEL_SCRIPT} "
            "TEMP_PATH/{{ params.output_file_crop }} "  
            "TEMP_PATH/{{ params.output_file_sobel }} "  
        ),
    )

    # Stage 3: Runs binarize.py
    binarize_task = BashOperator(
        task_id="binarize",
        bash_command=(
            f"python3 {BINARIZE_SCRIPT} "
            "TEMP_PATH/{{ params.output_file_sobel }} " 
            "{{ params.thresh }} " 
            "TEMP_PATH/{{ params.output_file_binarize }} "  
        ),
    )

    # Stage 4: Runs droplet_height.py
    height_task = BashOperator(
        task_id="droplet_height",
        bash_command=(
            f"python3 {HEIGHT_SCRIPT} "
            "TEMP_PATH/{{ params.output_file_binarize }} " 
            "OUT_PATH/{{ params.output_height }} "  
            "OUT_PATH/{{ params.output_file_hegiht }} "  
        ),
    )

    # Define the workflow dependency
    crop_task >> sobel_task >> binarize_task >> height_task

# Exapmle input
# {
#   "inpFile": "~/Projects/ImageBlobler/apache/input_data/10000.jpeg",
#   "start_x": 464,
#   "start_y": 193,
#   "crop_x": 169,
#   "crop_y": 154,
#   "output_file_crop": "crop_10000.jpeg",
#   "output_file_sobel": "sobel_10000.jpeg",
#   "thresh": 50,
#   "output_file_binarize": "binarize_10000.jpeg",
#   "output_file_hegiht": "height_10000.jpeg",
#   "output_height": "height_value_10000.txt"
# }