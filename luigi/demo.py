import luigi
from luigi import Task
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

class StageOne(luigi.Task):
    f1 = luigi.IntParameter(default=15)
    f2 = luigi.IntParameter(default=60)
    freq = luigi.IntParameter(default = 20)
    filename = luigi.Parameter(default='/home/mu2so4/univ/disser/hpc2c-seismics/segy/00000215_276_22_14.18.0.sgy')
    outFilename = luigi.Parameter(default=filteredPath)
    
    def run(self):
        data = readSEGY(self.filename)

        filtered = bandpass_filter(data, self.f1, self.f2)
        filtered2 = notch_filter(filtered, self.freq)
        with open(self.outFilename,'wb') as f:
            pickle.dump(filtered2, f)
    
    def output(self):
        return luigi.LocalTarget(self.outFilename)

class StageTwo(luigi.Task):
    freq2 = luigi.IntParameter(default = 40)
    freq3 = luigi.IntParameter(default = 50)
    outFilename = luigi.Parameter(default='filtered.segy')

    def requires(self):
        return StageOne()
    
    def run(self):
        #filename = self.input()
        with open(filteredPath,'rb') as f:
            initial_data = pickle.load(f)
        
        notched1 = notch_filter(initial_data, self.freq2)
        notched2 = notch_filter(notched1, self.freq3)
        visualize(notched2, "out_fin.png")
        writeSEGY(notched2, self.outFilename)
    
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(self.outFilename)


if __name__ == '__main__':
    luigi.run()

