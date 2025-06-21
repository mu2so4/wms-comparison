#!/usr/bin/env python3
import os
import logging
from pathlib import Path
from argparse import ArgumentParser

logging.basicConfig(level=logging.DEBUG)

# --- Import Pegasus API ------------------------------------------------------
from Pegasus.api import *


class SplitWorkflow:
    wf = None
    sc = None
    tc = None
    rc = None
    props = None

    dagfile = None
    wf_name = None
    wf_dir = None

    # --- Init ----------------------------------------------------------------
    def __init__(self, dagfile="workflow.yml"):
        self.dagfile = dagfile
        self.wf_name = "seismic"
        self.wf_dir = str(Path(__file__).parent.resolve())

    # --- Write files in directory --------------------------------------------
    def write(self):
        if not self.sc is None:
            self.sc.write()
        self.props.write()
        self.tc.write()
        self.rc.write()
        self.wf.write()

    # --- Configuration (Pegasus Properties) ----------------------------------
    def create_pegasus_properties(self):
        self.props = Properties()

        # props["pegasus.monitord.encoding"] = "json"
        # self.properties["pegasus.integrity.checking"] = "none"
        return

    # --- Site Catalog --------------------------------------------------------
    def create_sites_catalog(self, exec_site_name="condorpool"):
        self.sc = SiteCatalog()

        shared_scratch_dir = os.path.join(self.wf_dir, "scratch")
        local_storage_dir = os.path.join(self.wf_dir, "output")

        local = Site("local").add_directories(
            Directory(Directory.SHARED_SCRATCH, shared_scratch_dir).add_file_servers(
                FileServer("file://" + shared_scratch_dir, Operation.ALL)
            ),
            Directory(Directory.LOCAL_STORAGE, local_storage_dir).add_file_servers(
                FileServer("file://" + local_storage_dir, Operation.ALL)
            ),
        )

        exec_site = (
            Site(exec_site_name)
            .add_pegasus_profile(style="condor")
            .add_condor_profile(universe="vanilla")
            .add_profiles(Namespace.PEGASUS, key="data.configuration", value="condorio")
        )

        self.sc.add_sites(local, exec_site)

    # --- Transformation Catalog (Executables and Containers) -----------------
    def create_transformation_catalog(self, exec_site_name="condorpool"):
        self.tc = TransformationCatalog()

        wc = Transformation(
            "python", site=exec_site_name, pfn="/home/mu2so4/Documents/0Universe/disser/hpc2c-seismics/venv/bin/python", is_stageable=False,
        )

        self.tc.add_transformations(wc)

    # --- Replica Catalog ------------------------------------------------------
    def create_replica_catalog(self):
        self.rc = ReplicaCatalog()

        # Add f.a replica
        self.rc.add_replica(
            "local", "00000215_276_22_14.18.0.sgy", "/home/mu2so4/univ/disser/hpc2c-seismics/segy/00000215_276_22_14.18.0.sgy"
        )
        self.rc.add_replica(
            "local", "task1.py", "/home/mu2so4/univ/disser/cwl-pure/task1.py"
        )
        self.rc.add_replica(
            "local", "task2.py", "/home/mu2so4/univ/disser/cwl-pure/task2.py"
        )

    # --- Create Workflow -----------------------------------------------------
    def create_workflow(self):
        self.wf = Workflow(self.wf_name, infer_dependencies=True)

        sgy = File("00000215_276_22_14.18.0.sgy")
        sdFile = File("filtered2.sd")
        task1 = File("task1.py")
        task2 = File("task2.py")

        # the split job that splits the webpage into smaller chunks
        preprocessing = (
            Job("python")
            .add_args(task1, sgy, 15, 30, 20, sdFile)
            .add_inputs(sgy, task1)
            .add_pegasus_profile(label="p1")
        )
        
        preprocessing.add_outputs(sdFile, stage_out=True, register_replica=True)
        outSgy = File("filtered.sgy")
        outPic = File("result.png")

        postprocessing = (
            Job("python")
            .add_args(task2, sdFile, 40, 50, outPic, outSgy)
            .add_inputs(sdFile, task2)
            .set_stdout(outPic, stage_out=True, register_replica=True)
            .add_pegasus_profile(label="p1")
        )
        postprocessing.add_outputs(outSgy, stage_out=True, register_replica=True)
        #postprocessing.add_outputs(outPic, stage_out=True, register_replica=True)

        self.wf.add_jobs(preprocessing)
        self.wf.add_jobs(postprocessing)


if __name__ == "__main__":
    parser = ArgumentParser(description="Pegasus SGY Workflow")

    parser.add_argument(
        "-s",
        "--skip_sites_catalog",
        action="store_true",
        help="Skip site catalog creation",
    )
    parser.add_argument(
        "-e",
        "--execution_site_name",
        metavar="STR",
        type=str,
        default="condorpool",
        help="Execution site name (default: condorpool)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="STR",
        type=str,
        default="workflow.yml",
        help="Output file (default: workflow.yml)",
    )

    args = parser.parse_args()

    workflow = SplitWorkflow(args.output)

    if not args.skip_sites_catalog:
        print("Creating execution sites...")
        workflow.create_sites_catalog(args.execution_site_name)

    print("Creating workflow properties...")
    workflow.create_pegasus_properties()   
    
    print("Creating transformation catalog...")
    workflow.create_transformation_catalog(args.execution_site_name)

    print("Creating replica catalog...")
    workflow.create_replica_catalog()

    print("Creating split workflow dag...")
    workflow.create_workflow()

    workflow.write()
