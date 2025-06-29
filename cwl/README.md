# Common Workflow Language (CWL) Definitions

## Overview

The [Common Workflow Language (CWL)](https://www.commonwl.org/) is an open standard for describing computational data analysis workflows. Using YAML or JSON, CWL provides a specification for defining tools and workflows that are reproducible, portable, and interoperable across different execution environments.

A key purpose of CWL is portability. A workflow defined in CWL can be executed by numerous supporting Workflow Management Systems (WMS), including:
* **cwltool** (the reference implementation)
* **Toil**
* **Arvados**
* **Rabix**
* **Apache Airflow** (via community parsers like `cwl-airflow`)
* **Pegasus** (limited)
* **Galaxy**
* ... and others.

This allows researchers to describe their computational steps independently of any specific platform. However, as discovered during the development of this repository, achieving seamless portability in practice can still present significant challenges, often requiring minor or major adjustments for each target WMS.

## CWL Version
> **Note:** All workflows in this repository are defined using **CWL v1.1**.
>
> This version was chosen specifically for its broader compatibility across the range of benchmarked systems. Many WMS have not yet fully adopted the newer v1.2 standard, making v1.1 a more reliable choice for interoperability tests.

## Workflow Implementations
This directory provides two distinct CWL implementations of the benchmark workflow, each tailored for a different execution environment.

### Native Execution (`native/`)
This version is designed for running the workflow tasks directly on the host machine. The `CommandLineTool` definitions invoke the Python interpreter and scripts located in the `src/` directory.

### Containerized Execution (`containerized/`)
This version is designed for running the workflow tasks inside containers. The `CommandLineTool` definitions in this variant include a `DockerRequirement` directive, pointing to the pre-built images on Docker Hub. This allows any container-aware WMS to pull the correct image (for Docker or Apptainer/Singularity) and execute the task within it.

## Directory Structure
The contents of the `native/` and `containerized/` subdirectories are identical in structure:

* **`task1.cwl` & `task2.cwl`**: These files define the individual steps of the workflow as `CommandLineTool`s. They specify the command, inputs, and outputs for each task.
* **`workflow.cwl`**: This is the main workflow file. It imports `task1.cwl` and `task2.cwl` and chains them together, defining the data flow from the workflow inputs, through `task1`, and into `task2`.
* **`workflow_single_file.cwl`**: This is a self-contained version that combines the definitions from the three files above into a single document. It is functionally identical to running `workflow.cwl` and is provided for convenience or for systems that prefer a single entrypoint file.
* **`params.yml`**: An example input object file. It defines the parameters (like input file paths and filter settings) needed to execute the workflow.

## Example Usage with `cwltool`

To test these CWL definitions with the [reference implementation](../benchmarks/cwltool/README.md), you can run the following command from the `cwl/` directory:

```bash
# To run the native version
cwltool native/workflow.cwl native/params.yml
```

```bash
# To run the containerized version (requires Docker or Apptainer), remove the --singularity key to run via Docker
cwltool --singularity containerized/workflow.cwl containerized/params.yml
```
