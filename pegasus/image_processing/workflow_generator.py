#!/usr/bin/env python3
import os
import logging
from pathlib import Path
from argparse import ArgumentParser
import yaml

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
        self.wf_name = "image_processing"
        self.wf_dir = str(Path(__file__).parent.resolve())

    def get_next_file_name(self, prevFile: str, operationName: str):
        fileSplit = prevFile.split("/")
        return f"{fileSplit[fileSplit.__len__()-1]}" 

    def get_next_file_name_v2(self, prevFile: str, operationName: str):
        fileSplit = prevFile.split("/")
        return f"{operationName}_{fileSplit[fileSplit.__len__()-1]}" 

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
            "python", site=exec_site_name, pfn="/home/ilya/Projects/WMSs/wms-comparison/pegasus/pegasus-venv/bin/python", is_stageable=False,
        )

        self.tc.add_transformations(wc)

    # --- Replica Catalog ------------------------------------------------------
    def create_replica_catalog(self):
        self.rc = ReplicaCatalog()

        with open('params_full.yml', 'r') as f:
            parameters = yaml.safe_load(f)

        inp_files = parameters['images']
        for inp_file in inp_files: 
            fileSplit = inp_file['path'].split("/") 
            self.rc.add_replica(
                "local", inp_file['path'], fileSplit[fileSplit.__len__()-1]
            )

    # --- Create Workflow -----------------------------------------------------
    def create_workflow(self):
        self.wf = Workflow(self.wf_name, infer_dependencies=True)
        # Загрузка параметров из params.yml
        with open('params_full.yml', 'r') as f:
            parameters = yaml.safe_load(f)

        output_folder = '/home/ilya/Projects/WMSs/wms-comparison/pegasus/image_processing/output/'
        inp_files = parameters['images']

        for inp_file in inp_files:
            crop_script = parameters['crop_script']['path']
            start_x = parameters['start_x']
            start_y = parameters['start_y']
            crop_x = parameters['crop_x']
            crop_y = parameters['crop_y']
            out_crop_file_name = self.get_next_file_name(inp_file['path'], "crop")
            out_crop_real_file_name = self.get_next_file_name_v2(inp_file['path'], "crop")

            # crop_future = stage_crop_app(crop_script, inp_file['path'], start_x, start_y, crop_x, crop_y, out_crop_file_name,
            #                             outputs=[File(out_crop_real_file_name)])

            crop_task = (
                Job("python")
                .add_args(crop_script, inp_file['path'], start_x, start_y, crop_x, crop_y, out_crop_file_name)
                .add_pegasus_profile(label="p1")
            )
            crop_task.add_outputs(out_crop_real_file_name, stage_out=True, register_replica=True)
            self.wf.add_jobs(crop_task)

            sobel_script = parameters['sobel_script']['path']
            out_sobel_file_name = self.get_next_file_name(out_crop_file_name, "sobel") 
            out_sobel_real_file_name = self.get_next_file_name_v2(inp_file['path'], "sobel")

            sobel_task = (
                Job("python")
                .add_args(sobel_script, File(out_crop_real_file_name), out_sobel_file_name)
                .add_inputs(File(out_crop_real_file_name))
                .add_pegasus_profile(label="p1")
            )
            sobel_task.add_outputs(File(out_sobel_real_file_name), stage_out=True, register_replica=True)
            self.wf.add_jobs(sobel_task)

            binarize_script = parameters['binarize_script']['path']
            thresh = parameters['thresh']
            out_binarize_file_name = self.get_next_file_name(out_sobel_file_name, "binarize")
            out_binarize_real_file_name = self.get_next_file_name_v2(inp_file['path'], "binarize")

            binarize_task = (
                Job("python")
                .add_args(binarize_script, File(out_sobel_real_file_name), thresh, out_binarize_file_name)
                .add_inputs(File(out_sobel_real_file_name))
                .add_pegasus_profile(label="p1")
            )
            binarize_task.add_outputs(File(out_binarize_real_file_name), stage_out=True, register_replica=True)
            self.wf.add_jobs(binarize_task)

            droplet_height_script = parameters['droplet_height_script']['path']
            out_height_value_name = self.get_next_file_name(out_binarize_file_name, "droplet_height")
            out_height_value_real_file_name = (self.get_next_file_name_v2(inp_file['path'], "droplet_height")) + "_result.txt"
            out_height_file_name = self.get_next_file_name(out_binarize_file_name, "droplet_height")
            out_height_file__real_file_name = self.get_next_file_name_v2(inp_file['path'], "droplet_height")

            height_task = (
                Job("python")
                .add_args(droplet_height_script, File(out_binarize_real_file_name), out_height_value_name, out_height_file_name)
                .add_inputs(File(out_binarize_real_file_name))
                .add_pegasus_profile(label="p1")
            )
            height_task.add_outputs(File(out_height_value_real_file_name), stage_out=True, register_replica=True)
            height_task.add_outputs(File(out_height_file__real_file_name), stage_out=True, register_replica=True)
            self.wf.add_jobs(height_task)


if __name__ == "__main__":
    parser = ArgumentParser(description="Pegasus Image processing Workflow")

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
