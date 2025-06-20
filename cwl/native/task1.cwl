#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: CommandLineTool

baseCommand: python

inputs:
  script:
    type: File
    inputBinding:
      position: 1
  inpFile:
    type: File
    inputBinding:
      position: 2
  f1:
    type: int
    inputBinding:
      position: 3
  f2:
    type: int
    inputBinding:
      position: 4
  freq:
    type: int
    inputBinding:
      position: 5
  outPath:
    type: string
    default: filtered2.sd
    inputBinding:
      position: 6

outputs:
  filtered_data:
    type: File
    outputBinding:
      glob: $(inputs.outPath)
      
stdout: stdout.txt
