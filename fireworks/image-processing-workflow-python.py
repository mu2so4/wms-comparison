

from fireworks import ScriptTask
from fireworks.core.firework import Firework, Workflow
from fireworks.core.launchpad import LaunchPad
from fireworks.core.rocket_launcher import rapidfire

from pathlib import Path
import time


# Specify the directory path
directory = Path("image_processing_results")

# Create the folder (and parent folders if missing)
directory.mkdir(parents=True, exist_ok=True)

# set up the LaunchPad and reset it
launchpad = LaunchPad()
launchpad.reset('', require_password=False)


directory = Path('/home/ilya/Projects/WMSs/image_processing_input_data')

def get_next_file_path(prevFile: str, operationName: str):
    fileSplit = prevFile.split("/")
    return fileSplit[0] + "/" + operationName + fileSplit[1]  

fws = []
index = 0
for file in directory.iterdir():
    #if index > 0:
    #   break
    if file.is_file():
      # create the Workflow that passes job info
      fw1 = Firework([ScriptTask.from_str(f'python3 ../../image_processing/crop.py {file} 464 193 169 154 {"../image_processing_results/crop_" + file.name}')], spec={"_pass_job_info": True}, fw_id=(index*4) + 1)
      fw2 = Firework([ScriptTask.from_str(f'python3 ../../image_processing/sobel.py {"../image_processing_results/crop_" + file.name} {"../image_processing_results/sobel_crop_" + file.name}')], parents=[fw1], fw_id=(index*4) + 2)
      fw3 = Firework([ScriptTask.from_str(f'python3 ../../image_processing/binarize.py {"../image_processing_results/sobel_crop_" + file.name} 50 {"../image_processing_results/binarize_sobel_crop_" + file.name}')], parents=[fw2], fw_id=(index*4) + 3)
      fw4 = Firework([ScriptTask.from_str(f'python3 ../../image_processing/droplet_height.py {"../image_processing_results/binarize_sobel_crop_" + file.name} {"../image_processing_results/height_value_binarize_sobel_crop_" + file.name} {"../image_processing_results/height_file_binarize_sobel_crop_" + file.name}')], parents=[fw3], fw_id=(index*4) + 4)
      
      fws.append(fw1)
      fws.append(fw2)
      fws.append(fw3)
      fws.append(fw4)
      index = index + 1

wf = Workflow(fws)

# store workflow and launch it locally
launchpad.add_wf(wf)
start_time = time.perf_counter()
rapidfire(launchpad)
end_time = time.perf_counter()
print(f"Время выполнения: {end_time - start_time:.4f} секунд")

