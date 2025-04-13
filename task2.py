import segyio
import pickle
import numpy as np
import numpy.typing as npt
from scipy import signal
import pathlib
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class SeismicData:
#    dt: int
    traces: npt.NDArray



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

def visualize(data: SeismicData, filename) -> None:
    plt.imshow(data.traces[:, 14000:15000].T, vmin=-0.05, vmax=0.05)
    plt.savefig(filename)

def writeSEGY(data: SeismicData, path: str) -> None:
    spec = segyio.spec()
    spec.sorting = None
    spec.format = 5
    spec.samples = np.arange(1, data.traces.shape[1])
    spec.tracecount = data.traces.shape[0]
    with segyio.create(path, spec) as dst:
        #dst.text[0] = src.text[0]
        #dst.bin = src.bin
        #dst.header = src.header
        for i in range(spec.tracecount):
            dst.trace[i] = data.traces[i,:].astype(np.float32)


def StageTwo(filename, freq2=40, freq3=50, outPic="out_fin.png", outFile="filtered.segy"):
    with open(filename,'rb') as f:
        initial_data = pickle.load(f)
    
    notched1 = notch_filter(initial_data, freq2)
    notched2 = notch_filter(notched1, freq3)
    visualize(notched2, outPic)
    writeSEGY(notched2, outFile)

inputPath = 'filtered2.sd'

if __name__ == '__main__':
    StageTwo(inputPath)

