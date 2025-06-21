nextflow.enable.dsl=2

process TASK1 {
    
    container "mu2so4/seismic-filter-task:1.0.2"
    publishDir "${params.outdir}/task1"

    input:
    path inp_file
    val f1
    val f2
    val freq
    val out_path

    output:
    path out_path, emit: filtered_data

    script:
    def out_path = out_path != params.NULL_VALUE ? out_path : "filtered2.sd"
    """
    python /app/task1.py \
    ${inp_file} \
    ${f1} \
    ${f2} \
    ${freq} \
    ${out_path} \
    > stdout.txt
    """

}
