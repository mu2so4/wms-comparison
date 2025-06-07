#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: Workflow

requirements:
  InlineJavascriptRequirement: {}

inputs:
  script1: File
  script2: File
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
    run: task1.cwl
    in:
      script: script1
      inpFile: inpFile
      f1: f1
      f2: f2
      freq: freq
      outPath: out_stage1
    out: [filtered_data]

  stage2:
    run: task2.cwl
    in:
      script: script2
      filename: stage1/filtered_data
      freq2: freq2
      freq3: freq3
      outPic: out_pic
      outFile: out_segy
    out: [out_pic, out_file]
