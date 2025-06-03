import segyio
import pickle
import numpy as np
import numpy.typing as npt
from scipy import signal
from dataclasses import dataclass
import sys

@dataclass
class SeismicData:
#    dt: int
    traces: npt.NDArray

filteredPath = 'filtered2.sd'

def readSEGY(filename: str) -> SeismicData:
    with segyio.open(filename, ignore_geometry=True) as src:
        trace_data = [np.copy(tr) for tr in src.trace[:]]
        trace_data = np.stack(trace_data, axis=0)
        return SeismicData(trace_data)

def bandpass_filter(data: SeismicData, f1: int, f2: int) -> SeismicData:
    b, a = signal.butter(6, [f1,f2], 'bp', fs=1000)
    filtered = signal.filtfilt(b, a, data.traces, axis=1)
    return SeismicData(filtered)

def notch_filter(data: SeismicData, freq: int) -> SeismicData:
    b, a = signal.iirnotch(freq, 30, 1000)
    filtered = signal.filtfilt(b, a, data.traces, axis=1)
    return SeismicData(filtered)

def writeSEGY(data: SeismicData, path: str) -> None:
    spec = segyio.spec()
    spec.sorting = None
    spec.format = 5
    spec.samples = np.arange(1, data.traces.shape[1])
    spec.tracecount = data.traces.shape[0]
    with segyio.create(path, spec) as dst:
        for i in range(spec.tracecount):
            dst.trace[i] = data.traces[i,:].astype(np.float32)
    
def StageOne(filename='/home/mu2so4/univ/disser/hpc2c-seismics/segy/00000215_276_22_14.18.0.sgy', f1=15, f2=30, freq=20, outPath='filtered2.sd'):
    data = readSEGY(filename)
    filtered = bandpass_filter(data, f1, f2)
    filtered2 = notch_filter(filtered, freq)
    with open(outPath,'wb') as f:
        pickle.dump(filtered2, f)

if __name__ == '__main__':
    # Пример: python task1.py input.sgy 15 30 20 filtered2.sd
    if len(sys.argv) != 6:
        print("Usage: python task1.py <filename> <f1> <f2> <freq> <outPath>")
        sys.exit(1)
    filename = sys.argv[1]
    f1 = int(sys.argv[2])
    f2 = int(sys.argv[3])
    freq = int(sys.argv[4])
    outPath = sys.argv[5]
    StageOne(filename, f1, f2, freq, outPath)

