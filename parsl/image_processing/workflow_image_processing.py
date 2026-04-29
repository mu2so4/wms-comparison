import parsl
from parsl.app.app import bash_app
from parsl.data_provider.files import File
#from parsl.configs.local import local  # Используем локальную конфигурацию для примера

import yaml
import os

import time

# --- Parsl Приложения (Apps) ---

def get_next_file_name_v2(prevFile: str, operationName: str):
    fileSplit = prevFile.split("/")
    return f"{operationName}_{fileSplit[fileSplit.__len__()-1]}" 

def get_next_file_name(prevFile: str, operationName: str):
    fileSplit = prevFile.split("/")
    return f"{fileSplit[fileSplit.__len__()-1]}" 

@bash_app
def stage_crop_app(script, image, start_x, start_y, crop_x, crop_y, output_file, outputs,
               stdout: str = 'stdout_crop.txt', stderr: str = 'stderr_crop.txt'):
    return f"python3 {script} {image} {start_x} {start_y} {crop_x} {crop_y} {output_file}"

@bash_app
def stage_sobel_app(script, image, output_file, outputs,
               stdout: str = 'stdout_sobel.txt', stderr: str = 'stderr_sobel.txt'):
    return f"python3 {script} {image} {output_file}"

@bash_app
def stage_binarize_app(script, image, thresh, output_file, outputs,
               stdout: str = 'stdout_binarize.txt', stderr: str = 'stderr_binarize.txt'):
    return f"python3 {script} {image} {thresh} {output_file}"

@bash_app
def stage_height_app(script, image, height_output, output_file, outputs,
               stdout: str = 'stdout_height.txt', stderr: str = 'stderr_height.txt'):
    return f"python3 {script} {image} {height_output} {output_file}"

# --- Основной рабочий процесс Parsl ---
def main_workflow(parameters: dict):
    print(f"Запуск workflow с параметрами: {parameters}")

    # Параметры для stage1
    inp_files = parameters['images']

    value_future = []
    file_future = []

    for inp_file in inp_files:
        crop_script = parameters['crop_script']['path']
        start_x = parameters['start_x']
        start_y = parameters['start_y']
        crop_x = parameters['crop_x']
        crop_y = parameters['crop_y']
        out_crop_file_name = get_next_file_name(inp_file['path'], "crop")
        out_crop_real_file_name = get_next_file_name_v2(inp_file['path'], "crop")

        crop_future = stage_crop_app(crop_script, inp_file['path'], start_x, start_y, crop_x, crop_y, out_crop_file_name,
                                     outputs=[File(out_crop_real_file_name)])

        sobel_script = parameters['sobel_script']['path']
        out_sobel_file_name = get_next_file_name(out_crop_file_name, "sobel") 
        out_sobel_real_file_name = get_next_file_name_v2(inp_file['path'], "sobel")

        #print(f'Ouput from CROP: {crop_future.outputs[0]}')
        sobel_future = stage_sobel_app(sobel_script, crop_future.outputs[0].result(), out_sobel_file_name,
                                     outputs=[File(out_sobel_real_file_name)])

        binarize_script = parameters['binarize_script']['path']
        thresh = parameters['thresh']
        out_binarize_file_name = get_next_file_name(out_sobel_file_name, "binarize")
        out_binarize_real_file_name = get_next_file_name_v2(inp_file['path'], "binarize")

        #print(f'Ouput from SOBEL: {sobel_future.outputs[0]}')
        binarize_future = stage_binarize_app(binarize_script, sobel_future.outputs[0].result(), thresh, out_binarize_file_name,
                                     outputs=[File(out_binarize_real_file_name)])

        droplet_height_script = parameters['droplet_height_script']['path']
        out_height_value_name = get_next_file_name(out_binarize_file_name, "droplet_height")
        out_height_value_real_file_name = get_next_file_name_v2(inp_file['path'], "droplet_height")
        out_height_file_name = get_next_file_name(out_binarize_file_name, "droplet_height")
        out_height_file__real_file_name = get_next_file_name_v2(inp_file['path'], "droplet_height")

        #print(f'Ouput from BINARIZE: {binarize_future.outputs[0]}')
        height_future = stage_height_app(droplet_height_script, binarize_future.outputs[0].result(), out_height_value_name, out_height_file_name,
                                     outputs=[File(out_height_value_real_file_name), File(out_height_file__real_file_name)])

        # Ожидаем завершения всех задач и получаем итоговые File-объекты
        value_future.append(height_future.outputs[0])
        file_future.append(height_future.outputs[1])
        
    
    # Возвращаем фьючерсы на результаты
    return {
        "value": value_future,
        "file": file_future
    }

# --- Загрузка параметров и выполнение ---
if __name__ == "__main__":
    # Проверка наличия файла params.yml
    if not os.path.exists('params_small.yml'):
        print("Ошибка: Файл 'params_small.yml' не найден в текущей директории.")
        exit(1)

    # Загрузка параметров из params.yml
    with open('params_full.yml', 'r') as f:
        params = yaml.safe_load(f)

    print("Запуск рабочего процесса Parsl...")
    with parsl.load():
        # Выполнение рабочего процесса
        start_time = time.perf_counter()
        results_futures = main_workflow(params)

        # Ожидание завершения всех задач и получение путей к файлам
        value = results_futures['value']
        value_str = ','.join(map(lambda x: x.filepath, value))

        file = results_futures['file']
        file_str = ','.join(map(lambda x: x.filepath, file))
        end_time = time.perf_counter()
        print(f"Время выполнения: {end_time - start_time:.4f} секунд")

        print("\nРабочий процесс Parsl завершен.")
        print(f"Значение: {value_str}")
        print(f"Итоговый файл: {file_str}")
