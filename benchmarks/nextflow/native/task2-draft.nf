nextflow.enable.dsl=2

process TASK2 {
    
    //container "ubuntu:latest"
    publishDir "${params.outdir}/task2"

    input:
    path filename
    val freq2
    val freq3
    val out_file
    val out_pic

    output:
    path out_file, emit: out_file
    path out_pic, emit: out_pic

    script:
    """
    python \
    SRC_PATH/task2.py \
    ${filename} \
    ${freq2} \
    ${freq3} \
    ${out_pic} \
    ${out_file} \
    > stdout.txt
    """

}
