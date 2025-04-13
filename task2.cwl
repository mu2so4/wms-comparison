#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: CommandLineTool

baseCommand: python

inputs:
  filename:
    type: File
    inputBinding:
      position: 1
  freq2:
    type: int
    inputBinding:
      position: 2
  freq3:
    type: int
    inputBinding:
      position: 3
  outPic:
    type: string
    inputBinding:
      position: 4
  outFile:
    type: string
    inputBinding:
      position: 5

arguments: [/home/mu2so4/univ/disser/cwl-pure/task2.py]

outputs:
  out_pic:
    type: File
    outputBinding:
      glob: $(inputs.outPic)
  out_file:
    type: File
    outputBinding:
      glob: $(inputs.outFile)

stdout: stdout.txt
