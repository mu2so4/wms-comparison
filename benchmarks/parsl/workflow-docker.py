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


@bash_app

def stage1_app(in_file: str, f1: int, f2: int, freq: int, out_path: str,
    input_file_dir: str, output_file_dir: str, outputs):

    cmd = f"docker run -v {input_file_dir}:/app/data -v {output_file_dir}:/app/outputs mu2so4/seismic-filter-task:1.0.2 /app/data/{in_file} {f1} {f2} {freq} /app/outputs/{out_path}"
    print(f"Running {cmd}")
    return cmd


@bash_app
def stage2_app(filename: File, freq2: int, freq3: int, out_pic_path: str, out_file_path: str, outputs,
               stdout: str = 'stdout_stage2.txt', stderr: str = 'stderr_stage2.txt'):
    script_path = "../../src/task2.py"

    # CWL указывает позиционные аргументы: filename, freq2, freq3, outPic, outFile
    # Parsl автоматически позаботится о том, чтобы filename.filepath указывал на правильный файл
    return f"python {script_path} {filename.filepath} {freq2} {freq3} {out_pic_path} {out_file_path}"

# --- Основной рабочий процесс Parsl ---
def main_workflow(parameters: dict):
    print(f"Запуск workflow с параметрами: {parameters}")

    # Параметры для stage1
    inp_file = parameters['inpFile']
    f1_val = parameters['f1']
    f2_val = parameters['f2']
    freq_val = parameters['freq']
    out_stage1_file_name = parameters['out_stage1']
    
    out_stage1_short = os.path.basename(out_stage1_file_name)
    abs_input_file_path = os.path.abspath(inp_file)
    input_filename = os.path.basename(abs_input_file_path)
    input_dirname = os.path.dirname(abs_input_file_path)
    out_task1_dirname = os.path.abspath("docker-out-task1")

    # Запуск stage1
    # Объявляем out_stage1_file_name как выходной файл, чтобы Parsl мог его отслеживать
    print(f"Запуск stage1_app: input_filename={input_filename}, f1={f1_val}, f2={f2_val}, freq={freq_val}, outPath={out_stage1_short}, input_dirname={input_dirname}, out_task1_dirname={out_task1_dirname}")
    stage1_future = stage1_app(input_filename, f1_val, f2_val, freq_val, out_stage1_short, input_dirname, out_task1_dirname,
                                 outputs=[File(out_stage1_file_name)])

    # Параметры для stage2
    freq2_val = parameters['freq2']
    freq3_val = parameters['freq3']
    out_pic_file_name = parameters['out_pic']
    out_segy_file_name = parameters['out_segy']

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
        print("Ошибка: Файл 'params.yml' не найден в текущей директории.")
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
