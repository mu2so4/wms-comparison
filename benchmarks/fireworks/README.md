# FireWorks

**Version:** 2.0.4
**Website:** [https://materialsproject.github.io/fireworks/](https://materialsproject.github.io/fireworks/)

FireWorks is a dynamic workflow management system designed for high-throughput computation, especially in scientific research. It is used extensively in materials science and supports flexible execution of complex DAGs (Directed Acyclic Graphs) of jobs on local or distributed systems.

---

## Installation

**Required Python version:** 3.11

1. Ensure you are in the `fireworks` directory, which contains the `init.sh` script.
2. Run the installation:

```bash
chmod +x init.sh
./init.sh
```

This will set up a virtual environment `.fireworks-venv`, install FireWorks and its dependencies, and configure a local MongoDB instance for managing workflows.

---

## Usage

1. **Activate the environment**:

```bash
source .fireworks-venv/bin/activate
```

2. **Load the workflow**:

```bash
lpad add workflow.yaml
```

3. **Launch the workflow**:

```bash
rlaunch -s rapidfire
```

* `rapidfire`: runs all available jobs sequentially or in parallel (depending on configuration).
* `singleshot`: runs a single job and exits.

All output and logs will be saved in the local directory unless otherwise configured.

---

## Features

1. ✅ Uses **MongoDB** to store and manage workflows, tasks, and job history.
2. ✅ Supports **dynamic workflows** — jobs can spawn additional jobs during runtime.
3. ✅ Scales well to **clusters and supercomputers**, including support for SLURM, PBS, and custom job launchers.
4. ✅ CLI tools (`lpad`, `rlaunch`, `qlaunch`, etc.) offer fine-grained control over workflows.
5. ✅ Supports **workflow state tracking**, retries on failure, and job dependencies.
6. ⚠️ Requires configuration of **MongoDB**, even for local testing (handled by `init.sh` in this setup).
7. ⚠️ Workflow definitions (FireWorks) use a specific YAML or Python-based format, which may have a learning curve.

---
