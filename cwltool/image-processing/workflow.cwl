class: Workflow
cwlVersion: v1.2
doc: 'Droplet height workflow for collection'
inputs:
  images:
    type:
      type: array
      items: File
  crop_script: File
  sobel_script: File
  binarize_script: File
  droplet_height_script: File
  height_output: File
  start_x: int
  start_y: int
  crop_x: int
  crop_y: int
  thresh: int
outputs: 
  out:
    type: File[]
    outputSource: 4_Droplet/output_files
steps:
  1_Crop:
    run: cwl_tools/crop.cwl
    in:
      images: images
      script: crop_script
      start_x: start_x
      start_y: start_y
      crop_x: crop_x
      crop_y: crop_y
    out: [output_files]
  2_Sobel:
    run: cwl_tools/sobel.cwl
    in:
      images:
        source: 1_Crop/output_files
      script: sobel_script
    out: [output_files]
  3_Binarize:
    run: cwl_tools/binarize.cwl
    in:
      images: 
        source: 2_Sobel/output_files
      script: binarize_script
      thresh: thresh
    out: [output_files]
  4_Droplet:
    run: cwl_tools/droplet_height.cwl
    in:
      images: 
        source: 3_Binarize/output_files
      script: droplet_height_script
      height_output: height_output
    out: [output_files]


    