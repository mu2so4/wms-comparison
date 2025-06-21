import sys

parent_dir = ".."
sys.path.append(parent_dir)

import task1
import task2

import luigi
from luigi import Task

filteredPath = 'filtered2.sd'

class StageOne(luigi.Task):
    f1 = luigi.IntParameter(default=15)
    f2 = luigi.IntParameter(default=60)
    freq = luigi.IntParameter(default = 20)
    filename = luigi.Parameter(default='/home/mu2so4/univ/disser/hpc2c-seismics/segy/00000215_276_22_14.18.0.sgy')
    outFilename = luigi.Parameter(default=filteredPath)
    
    def run(self):
        task1.StageOne(self.filename, self.f1, self.f2, self.freq, self.outFilename)
    
    def output(self):
        return luigi.LocalTarget(self.outFilename)

class StageTwo(luigi.Task):
    freq2 = luigi.IntParameter(default = 40)
    freq3 = luigi.IntParameter(default = 50)
    outFilename = luigi.Parameter(default='filtered.segy')

    def requires(self):
        return StageOne()
    
    def run(self):
        task2.StageTwo(filteredPath)
    
    def output(self) -> luigi.LocalTarget:
        return luigi.LocalTarget(self.outFilename)


if __name__ == '__main__':
    luigi.run()

