#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool

baseCommand: python

inputs:
  inpFile:
    type: string
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

arguments: [/home/mu2so4/univ/disser/cwl-pure/task1.py]

outputs:
  filtered_data:
    type: File
    outputBinding:
      glob: $(inputs.outPath)
      
stdout: stdout.txt
