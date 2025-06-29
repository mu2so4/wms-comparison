import parsl
from parsl.app.app import bash_app
from parsl.data_provider.files import File
#from parsl.configs.local import local  # Используем локальную конфигурацию для примера

import yaml
import os

# Загрузка конфигурации Parsl
# Для простых локальных задач подойдет `local.config`.
# Для более сложных или распределенных систем может потребоваться более сложная конфигурация.
#parsl.load(local.config)

# --- Parsl Приложения (Apps) ---


def get_filename_and_dirname(filepath: str):
    full_filename = os.path.abspath(filepath)
    full_dirname = os.path.dirname(full_filename)
    filename = os.path.basename(full_filename)
    return filename, full_dirname

@bash_app
def stage1_app(in_filename: str, f1: int, f2: int, freq: int, out_filename: str,
    outputs):
    input_filename, input_file_dir = get_filename_and_dirname(in_filename)
    output_filename, output_file_dir = get_filename_and_dirname(out_filename)
    
    cmd = f"docker run -v {input_file_dir}:/app/data -v {output_file_dir}:/app/outputs mu2so4/seismic-filter-task:1.0.2 /app/data/{input_filename} {f1} {f2} {freq} /app/outputs/{output_filename}"
    print(f"Running {cmd}")
    return cmd


@bash_app
def stage2_app(filename: File, freq2: int, freq3: int, out_pic_path: str, out_file_path: str, outputs,
               stdout: str = 'stdout_stage2.txt', stderr: str = 'stderr_stage2.txt'):
    # Parsl автоматически позаботится о том, чтобы filename.filepath указывал на правильный файл
    input_filename, input_file_dir = get_filename_and_dirname(filename.filepath)
    output_pic_filename, output_pic_dir = get_filename_and_dirname(out_pic_path)
    output_segy_filename, _ = get_filename_and_dirname(out_file_path)

    # CWL указывает позиционные аргументы: filename, freq2, freq3, outPic, outFile
    cmd = f"docker run -v {input_file_dir}:/app/data -v {output_pic_dir}:/app/outputs mu2so4/seismic-processing-task:1.0.2 /app/data/{input_filename} {freq2} {freq3} /app/outputs/{output_pic_filename} /app/outputs/{output_segy_filename}"
    print(f"Running {cmd}")
    return cmd

# --- Основной рабочий процесс Parsl ---
def main_workflow(parameters: dict):
    print(f"Запуск workflow с параметрами: {parameters}")
    out_dir1 = 'out1-docker'
    out_dir2 = 'out2-docker'

    # Параметры для stage1
    inp_file = parameters['inpFile']
    f1_val = parameters['f1']
    f2_val = parameters['f2']
    freq_val = parameters['freq']
    out_stage1_file_name = os.path.join(out_dir1, "filtered.sd")

    # Запуск stage1
    # Объявляем out_stage1_file_name как выходной файл, чтобы Parsl мог его отслеживать
    print(f"Запуск stage1_app: inpFile={inp_file}, f1={f1_val}, f2={f2_val}, freq={freq_val}, outPath={out_stage1_file_name}")
    stage1_future = stage1_app(inp_file, f1_val, f2_val, freq_val, out_stage1_file_name,
                                 outputs=[File(out_stage1_file_name)])

    # Параметры для stage2
    freq2_val = parameters['freq2']
    freq3_val = parameters['freq3']
    out_pic_file_name = os.path.join(out_dir2, parameters['out_pic'])
    out_segy_file_name = os.path.join(out_dir2, parameters['out_segy'])

    # Запуск stage2
    # Передаем выходной файл из stage1 в качестве входного в stage2.
    # Parsl будет ждать завершения stage1 перед началом stage2.
    print(f"Запуск stage2_app: filename={stage1_future.outputs[0]}, freq2={freq2_val}, freq3={freq3_val}, outPic={out_pic_file_name}, outFile={out_segy_file_name}")
    stage2_future = stage2_app(filename=stage1_future.outputs[0],
                                 freq2=freq2_val,
                                 freq3=freq3_val,
                                 out_pic_path=out_pic_file_name,
                                 out_file_path=out_segy_file_name,
                                 outputs=[File(out_pic_file_name), File(out_segy_file_name)])

    # Ожидаем завершения всех задач и получаем итоговые File-объекты
    final_image_future = stage2_future.outputs[0]
    final_segy_future = stage2_future.outputs[1]
    
    # Возвращаем фьючерсы на результаты
    return {
        "final_image": final_image_future,
        "final_segy": final_segy_future
    }

# --- Загрузка параметров и выполнение ---
if __name__ == "__main__":
    # Проверка наличия файла params.yml
    if not os.path.exists('params.yml'):
        print("Ошибка: Файл 'params-docker.yml' не найден в текущей директории.")
        exit(1)

    # Загрузка параметров из params.yml
    with open('params.yml', 'r') as f:
        params = yaml.safe_load(f)

    print("Запуск рабочего процесса Parsl...")
    with parsl.load():
        # Выполнение рабочего процесса
        results_futures = main_workflow(params)

        # Ожидание завершения всех задач и получение путей к файлам
        final_image_path = results_futures['final_image'].result().filepath
        final_segy_path = results_futures['final_segy'].result().filepath

        print("\nРабочий процесс Parsl завершен.")
        print(f"Итоговое изображение: {final_image_path}")
        print(f"Итоговый файл SEGY: {final_segy_path}")
    #except Exception as e:
    #    print(f"Произошла ошибка во время выполнения рабочего процесса Parsl: {e}")
    #finally:
    #    parsl.cleanup()
    #    print("Очистка ресурсов Parsl завершена.")
