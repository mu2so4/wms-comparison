nextflow.enable.dsl=2

process TASK2 {
    
    container "mu2so4/seismic-processing-task:1.0.2"
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
    python /app/task2.py \
    ${filename} \
    ${freq2} \
    ${freq3} \
    ${out_pic} \
    ${out_file} \
    > stdout.txt
    """

}
