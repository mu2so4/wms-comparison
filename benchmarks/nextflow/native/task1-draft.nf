nextflow.enable.dsl=2

process TASK1 {
    
    //container "ubuntu:latest"
    publishDir "${params.outdir}/task1"

    input:
    val f1
    val f2
    val freq
    val inp_file
    val out_path

    output:
    path out_path, emit: filtered_data

    script:
    def out_path = out_path != params.NULL_VALUE ? out_path : "filtered2.sd"
    """
    python \
    SRC_PATH/task1.py \
    ${inp_file} \
    ${f1} \
    ${f2} \
    ${freq} \
    ${out_path} \
    > stdout.txt
    """

}
