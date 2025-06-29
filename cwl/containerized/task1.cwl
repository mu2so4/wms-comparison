#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull: mu2so4/seismic-filter-task:1.0.2

inputs:
  inpFile:
    type: File
    inputBinding:
      position: 1
  f1:
    type: int
    inputBinding:
      position: 2
  f2:
    type: int
    inputBinding:
      position: 3
  freq:
    type: int
    inputBinding:
      position: 4
  outPath:
    type: string
    default: filtered2.sd
    inputBinding:
      position: 5

outputs:
  filtered_data:
    type: File
    outputBinding:
      glob: $(inputs.outPath)
      
stdout: stdout.txt
