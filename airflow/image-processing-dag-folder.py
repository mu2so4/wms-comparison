from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.models import Param
import pendulum
import glob
import os

CROP_SCRIPT = "CROP_PATH"
SOBEL_SCRIPT = "SOBEL_PATH"
BINARIZE_SCRIPT = "BINARIZE_PATH"
HEIGHT_SCRIPT = "HEIGHT_PATH"

with DAG(
    dag_id="image-processing-parallel",
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["image processing", "parallel", "dynamic"],
    params={
        "input_folder": Param(
            type="string", 
            description="Path to folder with input images",
            default="/home/ilya/airflow/input"
        ),
        "start_x": Param(type="integer", default=0),
        "start_y": Param(type="integer", default=0),
        "crop_x": Param(type="integer", default=100),
        "crop_y": Param(type="integer", default=100),
        "thresh": Param(type="integer", default=128),
    },
) as dag:
    
    @task
    def get_image_files(input_folder: str):
        """Получает список всех изображений в папке"""
        # Поддерживаемые форматы
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.tiff', '*.bmp']
        files = []
        
        for ext in extensions:
            files.extend(glob.glob(os.path.join(input_folder, ext)))
        
        # Возвращаем только имена файлов (без полного пути)
        return [os.path.basename(f) for f in files]
    
    @task
    def process_single_image(file_name: str, **context):
        """Обрабатывает одно изображение через все этапы"""
        import subprocess
        
        # Формируем временные и выходные файлы для этого изображения
        base_name = os.path.splitext(file_name)[0]
        temp_crop = f"TEMP_PATH/{base_name}_crop.png"
        temp_sobel = f"TEMP_PATH/{base_name}_sobel.png"
        temp_bin = f"TEMP_PATH/{base_name}_bin.png"
        out_height = f"OUT_PATH/{base_name}_height.txt"
        out_image = f"OUT_PATH/{base_name}_final.png"
        
        # Этап 1: Crop
        crop_cmd = [
            "python3", CROP_SCRIPT,
            f"/home/ilya/Projects/WMSs/image_processing_input_data/{file_name}",
            str(context['params']['start_x']),
            str(context['params']['start_y']),
            str(context['params']['crop_x']),
            str(context['params']['crop_y']),
            temp_crop
        ]
        subprocess.run(crop_cmd, check=True)
        
        # Этап 2: Sobel
        sobel_cmd = [
            "python3", SOBEL_SCRIPT,
            temp_crop,
            temp_sobel
        ]
        subprocess.run(sobel_cmd, check=True)
        
        # Этап 3: Binarize
        binarize_cmd = [
            "python3", BINARIZE_SCRIPT,
            temp_sobel,
            str(context['params']['thresh']),
            temp_bin
        ]
        subprocess.run(binarize_cmd, check=True)
        
        # Этап 4: Height calculation
        height_cmd = [
            "python3", HEIGHT_SCRIPT,
            temp_bin,
            out_height,
            out_image
        ]
        subprocess.run(height_cmd, check=True)
        
        return f"Processed {file_name} successfully"
    
    # Получаем список файлов
    image_files = get_image_files("{{ params.input_folder }}")
    
    # Параллельно обрабатываем каждый файл
    # map() создаст отдельную задачу для каждого файла
    results = process_single_image.expand(file_name=image_files)

{
  "input_folder": "/home/ilya/Projects/WMSs/image_processing_input_data",
  "start_x": 464,
  "start_y": 193,
  "crop_x": 169,
  "crop_y": 154,
  "thresh": 50
}