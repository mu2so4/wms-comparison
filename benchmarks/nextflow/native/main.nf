nextflow.enable.dsl=2

include { TASK1 as STAGE1 } from './task1'
include { TASK2 as STAGE2 } from './task2'


workflow {

    STAGE1(
        params.f1,
        params.f2,
        params.freq,
        params.inp_file,
        params.out_stage1
    )

    STAGE2(
        STAGE1.out.filtered_data,
        params.freq2,
        params.freq3,
        params.out_segy,
        params.out_pic
    )


}
