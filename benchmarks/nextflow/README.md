# Nextflow

| Characteristic      | Value                                                                             |
| ------------------- | --------------------------------------------------------------------------------- |
| Primary Language    | Nextflow DSL2                                                                     |
| Paradigm            | Data-flow                                                                         |
| CWL Support         | Partial transpilation via [Janis Library](https://janis.readthedocs.io/en/latest/) |
| Docker Support      | [Native](https://www.nextflow.io/docs/latest/container.html#docker)            |
| Apptainer Support   | [Native](https://www.nextflow.io/docs/latest/container.html#apptainer)         |
| Interface Type      | CLI                                                                               |
| Cluster Support     | [Native](https://www.nextflow.io/docs/latest/executor.html), [Cloud](https://seqera.io/)      |

## Description

[Nextflow](https://www.nextflow.io) is a workflow management system that simplifies writing and deploying data-intensive, containerised pipelines in a portable and scalable manner. It supports a wide variety of execution platforms, including local machines, HPC schedulers (e.g., SLURM, PBS, HTCondor), Kubernetes, and major cloud providers (AWS, Azure, Google Cloud).

Nextflow is particularly dominant in the field of bioinformatics, supported by a large and active community, [nf-core](https://nf-co.re/), which develops and curates a collection of production-ready, best-practice analysis pipelines.

## Installation

To install Nextflow and its dependencies for this benchmark, run the initialization script.

```bash
bash ./init.sh
```

This script will:

1.  Download the Nextflow executable into a local `bin/` directory.
2.  Create a Python virtual environment at `.nextflow-venv` and install the `janis-pipelines` library, which is used for CWL translation.

You can optionally move the `nextflow` binary to a directory in your system's `$PATH` (e.g., `/usr/local/bin`) for global access.

## Usage

Nextflow's configuration is highly flexible. For examples of configurations for various HPC and cloud systems, the [nf-core/configs](https://github.com/nf-core/configs) repository is an excellent resource.

  * **Local Execution:**
    ```bash
    bash ./run.sh
    ```
  * **Apptainer / Singularity Execution:**
    ```bash
    bash ./run-singularity.sh
    ```

### Output Structure

After a run, Nextflow creates several outputs:

  * `work/`: A directory containing the intermediate files and scripts for each task. It's useful for debugging.
  * `outputs/`: Symlinks to the final result files are placed here for easy access.
  * `.nextflow.log`: The main log file for the most recent run. Previous log files are rotated (e.g., `.nextflow.log.1`, `.nextflow.log.2`).

## Key Implementation Details

### CWL to Nextflow Conversion using Janis

The [Janis](https://janis.readthedocs.io/en/latest/) library provides a way to transpile workflows from CWL to Nextflow's DSL2. Janis generates a main `.nf` script and a `nextflow.config` file.

**Example translation command** (run within the activated `.nextflow-venv`):

```bash
janis translate --from cwl --to nextflow ../../cwl/native/workflow.cwl
```

  * `--from cwl`: Source language (also supports [WDL](https://openwdl.org/) and [Galaxy](../galaxy/README.md)).
  * `--to nextflow`: Target language (also supports CWL and WDL).
  * The final argument is the path to the source CWL file.

**Key Findings and Quirks:**
Our evaluation of the translation process revealed the following:

1.  **Forced Container:** When translating a workflow without containers, Janis inserts a default `container "ubuntu:latest"` directive into each process. This occurs even when using the `--disallow-empty-container` flag. You may need to manually remove these lines from the generated `*.nf` file for a truly local execution.
2.  **Ignored `ENTRYPOINT`:** When translating a containerized CWL workflow, Janis does not carry over the `ENTRYPOINT` command from the Docker image definition. This means you must manually add the command to the `script` block of each process in the Nextflow workflow.

### Containerized Execution

Nextflow has excellent native [support](https://www.nextflow.io/docs/latest/container.html) for various container platforms.

#### Apptainer / Singularity

To enable Apptainer, add the following to your `nextflow.config` file. Janis typically does this automatically during translation.

```groovy
singularity.enabled = true
singularity.autoMounts = true // Optional: automatically mount common host directories
singularity.cacheDir = "$HOME/.singularity/cache" // Optional: specify a cache location
```

> **Reminder:** As noted above, Nextflow ignores the `ENTRYPOINT` of the container image. You must explicitly write the command to be executed in the `script` block of your process definition.

#### Docker

In our testing, we were unable to get the Docker execution to work using the same workflow definition that succeeded with Apptainer (after modifying the config from `singularity` to `docker`). An analysis of the community-provided `nf-core/configs` repository shows that Singularity/Apptainer is the predominantly used container engine for HPC environments, with Docker configurations being less common.

## Troubleshooting

  * **Log Rotation:** Remember that Nextflow rotates log files after each run. The most recent log is always `.nextflow.log`.
  * **`ENTRYPOINT` Issue:** If your containerized task fails silently or with an error, the first thing to check is whether you have explicitly included the container's `ENTRYPOINT` command in the `script` block of the Nextflow process.

## Pros & Cons

### Pros:

  * **Excellent Cluster Support:** Robust and flexible integration with a wide range of HPC schedulers.
  * **Implicit Parallelism:** The data-flow paradigm makes parallelization of tasks intuitive and automatic.
  * **Strong Community & Ecosystem:** The `nf-core` community provides a wealth of reusable, best-practice pipelines and tools.
  * **Powerful Caching:** Nextflow's caching is highly effective, preventing re-computation of unchanged tasks.
  * **Direct Path for CWL Conversion:** The Janis library provides a functional, if quirky, tool for translating CWL workflows.

### Cons:

  * **Potential Docker Issues:** As noted, running with Docker may require more specific configuration compared to Apptainer/Singularity in certain environments.
  * **Translation Quirks:** The CWL-to-Nextflow translation via Janis requires manual post-processing to handle container directives and `ENTRYPOINT` issues.
