#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs:
  inpFile: File
  f1: int
  f2: int
  freq: int
  freq2: int
  freq3: int
  out_stage1: string
  out_pic: string
  out_segy: string

outputs:
  final_image:
    type: File
    outputSource: stage2/out_pic
  final_segy:
    type: File
    outputSource: stage2/out_file

steps:
  stage1:
    run:
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
    in:
      inpFile: inpFile
      f1: f1
      f2: f2
      freq: freq
      outPath: out_stage1
    out: [filtered_data]

  stage2:
    run:
      cwlVersion: v1.1
      class: CommandLineTool

      requirements:
        DockerRequirement:
            dockerPull: mu2so4/seismic-processing-task:1.0.2

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
    in:
      filename: stage1/filtered_data
      freq2: freq2
      freq3: freq3
      outPic: out_pic
      outFile: out_segy
    out: [out_pic, out_file]
