# Parsl

| Characteristic      | Value                               |
| ------------------- | -------------------------------------- |
| Primary Language    | Python                                 |
| Paradigm            | Control-flow                           |
| CWL Support         | Limited ([CWL-Parsl](https://github.com/Parsl/cwl-parsl), early development) |
| Docker Support      | Limited (via `@bash_app` wrapper)      |
| Apptainer Support   | Limited (via `@bash_app` wrapper)      |
| Cluster Support     | Yes, e.g., [HTCondor Provider](https://parsl.readthedocs.io/en/desc/stubs/parsl.providers.CondorProvider.html) |

## Description
[Parsl](https://parsl-project.org/) is a Python library designed for parallel and distributed computing. It enables developers to write workflows in pure Python and execute them seamlessly on resources ranging from a local laptop to large HPC clusters. Parsl is widely used in scientific domains such as physics, bioinformatics, and chemistry to orchestrate complex computational tasks.

## Installation
To install Parsl and its dependencies for this benchmark, run the initialization script in this directory.

```bash
bash ./init.sh
```

This script will create a dedicated Python virtual environment at `.parsl-venv` and install all necessary packages, including Parsl itself.

## Usage
### Local Execution:
```
bash ./run.sh
```

This will execute the workflow locally using Parsl. The output files will be generated in the current directory, and detailed logs will be written to the `runinfo/` subdirectory.

### Containerized Execution:
Native support for Docker or Apptainer is limited. For this benchmark, containerized execution is implemented using Parsl's `@bash_app` decorator to wrap `docker run` or `singularity run` commands. See the "Key Implementation Details" section for code examples.

## Key Implementation Details

### CWL Support and Conversion

A library named [CWL-Parsl](https://github.com/Parsl/cwl-parsl) exists to convert CWL files into Parsl-compatible Python code. However, our evaluation found it to be in an early stage of development with significant limitations. For example, it does not correctly process `class: Workflow` definitions and ignores the `arguments` block in tool definitions.

Given these constraints, we recommend either **manually rewriting** the CWL logic in Python for Parsl or using an **LLM (e.g., ChatGPT, Gemini)** to assist with the conversion.

### Executing Docker & Apptainer Tasks

While Parsl does not have built-in executors for Docker or Apptainer like some other WMS, it is flexible enough to support them indirectly using the `@bash_app` decorator. This decorator allows you to define a workflow task as a shell command.

**Example for Docker**
```python
@bash_app
def stage1_app(in_file: str, f1: int, f2: int, freq: int, out_path: str,
               input_file_dir: str, output_file_dir: str, outputs):
    
    return f"docker run -v {input_file_dir}:/app/data -v {output_file_dir}:/app/outputs mu2so4/seismic-filter-task:1.0.2 /app/data/{in_file} {f1} {f2} {freq} /app/outputs/{out_path}"
```

* `input_file_dir`: The absolute path to the `inputs/` directory of this repository.
* `output_file_dir`: The absolute path to the directory where the output file will be written (e.g., an `outputs/` directory inside this folder).
* Other parameters are passed directly to the task. Note that `in_file` should be just the filename (e.g., `input.sgy`).

**Example for Apptainer**
The parameters are the same as in the Docker example.
> Note: You must create the output directory (output_file_dir) manually before running the workflow, as Apptainer will not create it for you when binding a mount.

## Troubleshooting
### 💡 Finding the Latest Documentation

Be aware that the official Parsl documentation website often defaults to an older version (e.g., 1.3.0 from 2022). The project is actively maintained. To access the **latest documentation**, use the version switcher on the bottom-right of the page and select the desc branch.

[Link to the latest (desc) documentation](https://parsl.readthedocs.io/en/desc/)

## Pros and Cons
### Pros
* **Native Parallelism**: Excellent support for creating and managing parallel tasks in Python.
* **HPC Ready**: Strong support for various cluster schedulers (e.g., Slurm, HTCondor), making it easy to scale from a laptop to a supercomputer.
* **Python-Native DAGs**: Workflows are defined directly in Python, eliminating the need for separate configuration or DSL files.
* **Caching**: Automatically caches results, preventing re-computation of tasks if inputs and code have not changed.

### Cons
* **Limited CWL Support**: The existing tools for CWL integration are immature and not suitable for complex workflows.

* **No Native Container Integration**: Lacks built-in executors for Docker or Apptainer, requiring manual wrapping of commands.
