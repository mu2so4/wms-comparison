import sys
import os
from pathlib import Path
import time

parent_dir = ".."
sys.path.append(parent_dir)

import luigi
from luigi import Task

input_folder = "/home/ilya/Projects/WMSs/image_processing_input_data"

def get_next_file_path(prevFile: str, operationName: str):
    fileSplit = prevFile.split("/")
    return fileSplit[0] + "/" + operationName + fileSplit[1]  

def get_next_file_name(prevFile: str, operationName: str):
    fileSplit = prevFile.split("/")
    return f"./image_processing_results/{operationName}_{fileSplit[fileSplit.__len__()-1]}" 

class StageCrop(luigi.Task):
    input_file = luigi.Parameter()
    start_x = luigi.IntParameter(default=464)
    start_y = luigi.IntParameter(default=193)
    crop_x = luigi.IntParameter(default=169)
    crop_y = luigi.IntParameter(default=154)
    output_file = luigi.Parameter(default='./image_processing_results/crop.png')

    def run(self):
        self.output_file = get_next_file_name(self.input_file, "crop")
        os.system(f'python3 ../image_processing/crop.py {self.input_file} {self.start_x} {self.start_y} {self.crop_x} {self.crop_y} {self.output_file}')
    
    def output(self):
        return luigi.LocalTarget(self.output_file)

class StageSobel(luigi.Task):
    input_file = luigi.Parameter()
    output_file = luigi.Parameter(default='./image_processing_results/sobel.png')

    def requires(self):
        return StageCrop(input_file=self.input_file)
    
    def run(self):
        self.output_file = get_next_file_name(self.input_file, "sobel")
        os.system(f'python3 ../image_processing/sobel.py {self.input()} {self.output_file}')
    
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(self.output_file)
    
class StageBinarize(luigi.Task):
    input_file = luigi.Parameter()
    threash = luigi.IntParameter(default=50)
    output_file = luigi.Parameter(default='./image_processing_results/binarize.png')

    def requires(self):
        return StageSobel(input_file=self.input_file)
    
    def run(self):
        self.output_file = get_next_file_name(self.input_file, "binarize")
        os.system(f'python3 ../image_processing/binarize.py {self.input()} {self.threash} {self.output_file}')
    
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(self.output_file)

    
class StageHeight(luigi.Task):
    input_file = luigi.Parameter()
    output_value = luigi.Parameter(default='./image_processing_results/height.txt')
    output_file = luigi.Parameter(default='./image_processing_results/height.png')

    def requires(self):
        return StageBinarize(input_file=self.input_file)
    
    def run(self):
        self.output_value = get_next_file_name(self.input_file, "height_value")
        self.output_file = get_next_file_name(self.input_file, "height")
        os.system(f'python3 ../image_processing/droplet_height.py {self.input()} {self.output_value} {self.output_file}')
    
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(self.output_file)


if __name__ == '__main__':
    # Specify the directory path
    directory = Path("image_processing_results")

    # Create the folder (and parent folders if missing)
    directory.mkdir(parents=True, exist_ok=True)

    directory = Path('/home/ilya/Projects/WMSs/image_processing_input_data')

    # /home/ilya/Projects/WMSs/image_processing_input_data/10000.jgeg

    index = 0
    start_time = time.perf_counter()
    for file in directory.iterdir():
        if file.is_file():
            luigi.build([
                StageHeight(input_file=str(file))
            ], local_scheduler=True)

    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time:.4f} секунд")


