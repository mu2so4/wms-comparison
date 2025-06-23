import os
import sys
import statistics as st

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} numbers.txt")
        sys.exit(1)
        
    wms_index = 0
    container_platform_index = 1
    numbers = []
    with open(sys.argv[1], 'r') as f:
        for index, line in enumerate(f):
            if index == wms_index:
                wms_name = line
            elif index == container_platform_index:
                container_platform_name = line
            else:
                numbers.append(float(line))
    
    mean = st.mean(numbers)
    stddev = st.stdev(numbers)
    
    print(wms_name)
    print(container_platform_name)
    print(f'Mean: {mean:.3f}')
    print(f'Std dev: {stddev:.3f}')
