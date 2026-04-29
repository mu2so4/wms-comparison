// /home/ilya/nextflow-25.10.4-dist run -params-file workflow.yml ./main.nf
//nextflow.enable.dsl=2

include { CROP } from './modules/crop'
include { SOBEL } from './modules/sobel'
include { BINARIZE } from './modules/binarize'
include { DROPLET_HEIGHT } from './modules/droplet_height'

// data which will be passed as variables
binarize_script        = params.binarize_script.path
crop_script            = params.crop_script.path
droplet_height_script  = params.droplet_height_script.path
height_output          = params.height_output.path
sobel_script           = params.sobel_script.path


workflow {

    CROP(
        params.images,
        crop_script,
        params.crop_x,
        params.crop_y,
        params.start_x,
        params.start_y
    )

    SOBEL(
        CROP.out.output_files,
        sobel_script
    )

    BINARIZE(
        SOBEL.out.output_files,
        binarize_script,
        params.thresh
    )

    DROPLET_HEIGHT(
        BINARIZE.out.output_files,
        height_output,
        droplet_height_script
    )
}
