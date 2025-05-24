import sys
import time

parent_dir = ".."
sys.path.append(parent_dir)

import task1
import task2

if __name__ == '__main__':
    intermediate_path = 'filtered.sd'
    print("Running task 1")
    start = time.process_time()
    task1.StageOne(outPath = intermediate_path)
    task1_end = time.process_time()
    print("Running task 2")
    task2.StageTwo(intermediate_path)
    task2_end = time.process_time()

    print("Elapsed time:")
    print(f"Task1: {(task1_end - start):.3f} s")
    print(f"Task2: {(task2_end - task1_end):.3f} s")
    print(f"Total: {(task2_end - start):.3f} s")
    
