# Workflow Task Images

## Overview

This directory contains the necessary files to build the container images for the two tasks (`task1`, `task2`) that constitute the benchmark workflow.

For this project, we provide support for two leading containerization technologies, allowing the workflow to be executed in various environments from local machines to High-Performance Computing (HPC) clusters.

* **Docker:** The most widely adopted container platform, ideal for development and service-oriented workloads. While powerful, its default requirement for root privileges can be a limitation in some secure or multi-user environments.
* **Apptainer (formerly Singularity):** A container platform tailored for HPC and scientific computing. It features rootless execution, compatibility with Docker images, and its native Singularity Image Format (SIF) is optimized for performance and security on shared systems.

## Directory Structure

This directory is organized by workflow task, with each subdirectory containing all the necessary assets to build an image for that specific task.

* `task1/`: Contains files for the first workflow task (`seismic-filter-task`).
* `task2/`: Contains files for the second workflow task (`seismic-processing-task`).

Inside each task directory, you will find:

1.  **`Dockerfile`**: The blueprint used to build the OCI-compliant container image. It specifies the base image, copies the task script, and installs dependencies from `requirements.txt`.
2.  **`requirements.txt`**: A minimal list of Python dependencies required for the task script.
3.  **`build-docker.sh`**: A convenience script to build the Docker image and tag it appropriately.
4.  **`build-singularity.sh`**: A script to build a Singularity Image Format (SIF) file from the locally-built Docker image. **This script must be run after the Docker image has been built.**

## Prerequisites and Installation

You must have Docker and/or Apptainer installed to build and run the images.

* **Docker:** Follow the [official installation guide](https://docs.docker.com/engine/install/) for your operating system.
* **Apptainer:** Follow the [official installation guide](https://apptainer.org/docs/admin/main/installation.html) for your operating system.

> **⚠️ Important Note for Debian/Ubuntu Users:**
> The official Apptainer installation instructions for Debian-based systems may omit two critical runtime dependencies: `squashfuse` and `gocryptfs`. These packages are required for optimal performance and stability. If they are missing, you may see `INFO` level logs (not `WARNING`s) mentioning them, and Apptainer may run significantly slower or produce unstable execution times.
>
> You can install them using `apt`:
> ```bash
> sudo apt-get update
> sudo apt-get install squashfuse gocryptfs
> ```

## How to Build the Images

To build the images locally, navigate to the desired task directory and execute the build scripts.

**Example for `task1`:**

1.  **Navigate to the task directory:**
    ```bash
    cd images/task1
    ```

2.  **Build the Docker image:**
    ```bash
    ./build-docker.sh
    ```

3.  **Build the Apptainer (SIF) image (optional):**
    *This requires the Docker image from the previous step.*
    ```bash
    ./build-singularity.sh
    ```

Repeat the process for the `task2` directory if needed.

## Pre-built Images on Docker Hub

For convenience, pre-built Docker images for both tasks are available on Docker Hub. Most of the WMS configurations in this repository are set up to pull these images automatically when running in Docker or Apptainer mode.

* **Task 1 (`seismic-filter-task`):**
    [`mu2so4/seismic-filter-task`](https://hub.docker.com/repository/docker/mu2so4/seismic-filter-task)
* **Task 2 (`seismic-processing-task`):**
    [`mu2so4/seismic-processing-task`](https://hub.docker.com/repository/docker/mu2so4/seismic-processing-task)
