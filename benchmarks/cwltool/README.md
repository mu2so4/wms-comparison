# cwltool

| Characteristic      | Value                                                                             |
| ------------------- | --------------------------------------------------------------------------------- |
| Primary Language    | CWL                                                                               |
| Paradigm            | Data-flow (defined by CWL)                                                        |
| CWL Support         | **Reference Implementation**                                                      |
| Docker Support      | [Native](https://www.commonwl.org/user_guide/topics/best-practices.html)          |
| Apptainer Support   | [Native](https://www.commonwl.org/user_guide/topics/best-practices.html)          |
| Interface Type      | CLI                                                                               |
| Remote Access       | No (local execution only)                                                         |
| Cluster Support     | No                                                                                |

## Description

[**cwltool**](https://github.com/common-workflow-language/cwltool) is the official reference implementation of the **Common Workflow Language (CWL)** standard. It is a Python-based tool designed to parse and execute CWL documents.

*Version used in this benchmark: `3.1.20250110105449`*

## Role in this Benchmark

As the reference implementation, `cwltool` served as the primary development and validation tool for the CWL documents in this repository. All workflows (`native/` and `containerized/`) were first tested and debugged using `cwltool` to ensure they were syntactically correct and functionally operational before being tested on other Workflow Management Systems.

## Installation

To install `cwltool` and its dependencies for this benchmark, run the initialization script.

```bash
bash ./init.sh
```

This script will create a Python virtual environment at `.cwltool-venv` and install the `cwltool` package using `pip`.

## Usage

  * **Local Execution:**
    ```bash
    bash ./run.sh
    ```
  * **Docker Execution:**
    ```bash
    bash ./run-docker.sh
    ```
  * **Apptainer / Singularity Execution:**
    ```bash
    bash ./run-singularity.sh
    ```

### Output Structure

After a successful run, `cwltool` creates the final workflow output files in the current working directory. It does not create intermediate directories like `work/`.

## Containerized Execution

`cwltool` has excellent native [support](https://www.commonwl.org/user_guide/topics/best-practices.html) for various container platforms. You can switch the container runtime by providing a command-line flag.

#### Executing with Docker (Default)

Docker is the default container runtime. No special flag is needed.

```bash
cwltool ../../cwl/containerized/workflow.cwl params-containerized.yml
```

#### Executing with Apptainer / Singularity

To use Apptainer or Singularity, add the `--singularity` flag.

```bash
cwltool --singularity ../../cwl/containerized/workflow.cwl params-containerized.yml
```

## Pros & Cons

### Pros

  * **CWL Reference Implementation:** Guarantees the most accurate and up-to-date support for the CWL standard. It is the definitive tool for validating CWL.
  * **Broad Container Support:** Natively works with a wide range of container platforms, including Docker, Apptainer/Singularity, Podman, and uDocker.

### Cons

  * **No Cluster Orchestration:** `cwltool` is designed for single-machine execution only. It cannot natively distribute tasks across a compute cluster. To run on an HPC system, one would typically need a higher-level tool to submit the `cwltool` command itself as a single cluster job.
