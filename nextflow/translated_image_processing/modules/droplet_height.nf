nextflow.enable.dsl=2

process DROPLET_HEIGHT {
    input:
    val images
    val height_output
    val script

    output:
    path "*.*", emit: output_files

    script:
    def cmd = ""
    images.forEach((image) -> { 
        def split = image.toString().split("/")
        def output_file = split[split.size()-1]
        cmd = cmd + "\n" + "python3 ${script} ${image} ${height_output} ${output_file}"
    })
    """
    ${cmd}
    """
}
