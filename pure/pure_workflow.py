import sys

parent_dir = "../src"
sys.path.append(parent_dir)

import task1
import task2

if __name__ == '__main__':
    intermediate_path = 'filtered.sd'
    print("Running task 1")
    task1.StageOne(outPath = intermediate_path)
    print("Running task 2")
    task2.StageTwo(intermediate_path)
    print("Execution terminated")
