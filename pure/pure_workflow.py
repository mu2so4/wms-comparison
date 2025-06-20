import sys

parent_dir = "../src"
sys.path.append(parent_dir)

import task1
import task2

if __name__ == '__main__':
    scriptPath = sys.argv[0]
    if len(sys.argv) != 10:
        print(f"Usage: python {scriptPath} <filename> <f1> <f2> <freq> <intermediatePath> <freq2> <freq3> <outPic> <outFile>")
        sys.exit(1)
    filename = sys.argv[1]
    f1 = int(sys.argv[2])
    f2 = int(sys.argv[3])
    freq = int(sys.argv[4])
    intermPath = sys.argv[5]
    freq2 = int(sys.argv[6])
    freq3 = int(sys.argv[7])
    outPic = sys.argv[8]
    outPath = sys.argv[9]
    task1.StageOne(filename, f1, f2, freq, intermPath)
    task2.StageTwo(intermPath, freq2, freq3, outPic, outPath)
