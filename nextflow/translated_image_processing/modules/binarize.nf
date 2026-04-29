nextflow.enable.dsl=2

process BINARIZE {
    input:
    val images
    val script
    val thresh

    output:
    path "*.jpeg", emit: output_files

    script:
    def cmd = ""
    images.forEach((image) -> { 
        def split = image.toString().split("/")
        def output_file = split[split.size()-1]
        cmd = cmd + "\n" + "python3 ${script} ${image} ${thresh} ${output_file}"
    })
    """
    ${cmd}
    """
}
