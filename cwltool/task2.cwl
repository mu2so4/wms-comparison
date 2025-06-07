#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: CommandLineTool

baseCommand: python

inputs:
  script:
    type: File
    inputBinding:
      position: 1
  filename:
    type: File
    inputBinding:
      position: 2
  freq2:
    type: int
    inputBinding:
      position: 3
  freq3:
    type: int
    inputBinding:
      position: 4
  outPic:
    type: string
    inputBinding:
      position: 5
  outFile:
    type: string
    inputBinding:
      position: 6

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
