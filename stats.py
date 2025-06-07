import os
import sys
import statistics as st

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} numbers.txt")
        sys.exit(1)
        
    numbers = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            numbers.append(float(line))
    
    mean = st.mean(numbers)
    stddev = st.stdev(numbers)
    
    print(f'Mean: {mean:.3f}')
    print(f'Std dev: {stddev:.3f}')
