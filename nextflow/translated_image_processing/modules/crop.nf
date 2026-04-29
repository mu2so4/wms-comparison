nextflow.enable.dsl=2

process CROP {
    input:
    val images
    val script
    val crop_x
    val crop_y
    val start_x
    val start_y

    output:
    path "*.jpeg", emit: output_files

    script:
    def cmd = ""
    images.forEach((image) -> { 
        def split = image.path.split("/")
        def output_file = split[split.size()-1]
        cmd = cmd + "\n" + "python3 ${script} ${image.path} ${start_x} ${start_y} ${crop_x} ${crop_y} ${output_file}"
    })
    """
    ${cmd}
    """
}